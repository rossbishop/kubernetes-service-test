"""Python Flask API Auth0 integration example
"""

from functools import wraps
import json
from os import environ as env
from six.moves.urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt

import time
from time import gmtime, strftime

import boto3
import uuid

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
#AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
AUTH0_DOMAIN = "dev-artsite.eu.auth0.com"
#API_IDENTIFIER = env.get("API_IDENTIFIER")
API_IDENTIFIER = "testapi"
ALGORITHMS = ["RS256"]
APP = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
# create dynamodb table object connected to projects table
table = dynamodb.Table('ArtShare-Projects')
tableName = "ArtShare-Projects"

# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, 401)
        if unverified_header["alg"] == "HS256":
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    " please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated


# REST API

# LOOK INTO SANITIZATION OF INCOMING DATA

@APP.route('/project/<id>', methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
def getProject(id):
    if request.method == "GET":
        response = table.get_item(
            TableName=tableName,
            Key={'id':str(id)}
        )
        return {
            'isBase64Encoded': "false",
            'statusCode': 200,
            'headers':{
                "Content-Type": "application/json"
            },
            'body': json.dumps(response['Item'])
        }
    else:
        return {"UWOTSUN": "That ain't right"}

@APP.route('/project/<id>', methods=["PUT", "DELETE"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def modifyProject(id):
    if request.method == "PUT":
        response = table.get_item(
            TableName=tableName,
            Key={'id':str(id)}
        )
    
        request.get_data()
        requestData = request.json

        # store the current time in a human readable format in a variable
        now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        #print(response['Item']['owner'])

        # Then check the owner name is the same as that in the access token
        #if response['Item']['owner'] == user['Username']:
        
        # Make the desired changes
        response = table.update_item(
            TableName=tableName,
            Key={'id':str(id)},
            UpdateExpression="set projectName = :pn, projectDescription = :pd, updatedAt = :t",
            ExpressionAttributeValues={
                ':pn': requestData['projectName'],
                ':pd': requestData['projectDescription'],
                ':t': now
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'isBase64Encoded': "false",
            'statusCode': 200,
            'headers':{
                "Content-Type": "application/json"
            },
            'body': json.dumps(response)
        }
    elif request.method == "DELETE":
        # First get the project
        response = table.get_item(
            TableName=tableName,
            Key={'id':str(id)}
        )
    
        # Then check the owner name is the same as that in the access token
        #if response['Item']['owner'] == user['Username']:

        # Make the deletion
        response = table.delete_item(
            TableName=tableName,
            Key={'id':str(id)}
        )
        return {
            'isBase64Encoded': "false",
            'statusCode': 200,
            'headers':{
                "Content-Type": "application/json"
            },
            'body': json.dumps(response)
        }
    else:
        return {"UWOTSUN": "That ain't right"}

@APP.route('/project', methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def createProject():
    if request.method == "POST":
        request.get_data()
        requestData = request.json

        # store the current time in a human readable format in a variable
        now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        id = uuid.uuid4()
        owner = "Jeff"
        projectName = requestData['projectName']
        projectDescription = requestData['projectDescription']
        contentType = "project"
        createdAt = now
        updatedAt = now
        
        # write name and time to the DynamoDB table using the object we instantiated and save response in a variable
        response = table.put_item(
            Item={
                'id': str(id),
                'owner': owner,
                'projectName': projectName,
                'projectDescription': projectDescription,
                'contentType': contentType,
                'createdAt': createdAt,
                'updatedAt': updatedAt
            })
        return {
            'isBase64Encoded': "false",
            'statusCode': 200,
            'headers':{
                "Content-Type": "application/json"
            },
            'body': str(id)
        }
    else:
        return {"UWOTSUN": "That ain't right"}

# Controllers API

@APP.route('/time')
@cross_origin(headers=["Content-Type", "Authorization"])
def get_current_time():
    return {'time': time.time()}

@APP.route("/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


@APP.route("/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)

@APP.route("/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("PORT", 3010))
