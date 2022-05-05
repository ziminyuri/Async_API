from http import HTTPStatus

import grpc
from fastapi import Depends, HTTPException

from grpc_client.client import get_stub
from grpc_client.stubs import auth_pb2, auth_pb2_grpc
from helpers import errors_dict, get_auth_token


def invalid_response(error):
    if error.code() == grpc.StatusCode.UNAUTHENTICATED:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=error.details())

    raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=errors_dict['503_grpc'])


def get_permissions(token: str = Depends(get_auth_token),
                    stub: auth_pb2_grpc.AuthStub = Depends(get_stub)):
    grpc_token = auth_pb2.Token(token=token)
    try:
        response = stub.GetPermissions(grpc_token)
        return response.permissions

    except grpc.RpcError as error:
        invalid_response(error)


def get_roles(token: str = Depends(get_auth_token),
              stub: auth_pb2_grpc.AuthStub = Depends(get_stub)):
    grpc_token = auth_pb2.Token(token=token)
    try:
        response = stub.GetRoles(grpc_token)
        return response.roles

    except grpc.RpcError as error:
        invalid_response(error)


def is_authenticated(token: str = Depends(get_auth_token),
                     stub: auth_pb2_grpc.AuthStub = Depends(get_stub)):
    grpc_token = auth_pb2.Token(token=token)
    try:
        response = stub.IsAuthorized(grpc_token)
        return response.is_valid

    except grpc.RpcError as error:
        invalid_response(error)
