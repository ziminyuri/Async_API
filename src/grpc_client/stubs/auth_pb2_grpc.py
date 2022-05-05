# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import auth_pb2 as auth__pb2


class AuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetPermissions = channel.unary_unary(
                '/gateway_backend.Auth/GetPermissions',
                request_serializer=auth__pb2.Token.SerializeToString,
                response_deserializer=auth__pb2.Permissions.FromString,
                )
        self.GetRoles = channel.unary_unary(
                '/gateway_backend.Auth/GetRoles',
                request_serializer=auth__pb2.Token.SerializeToString,
                response_deserializer=auth__pb2.Roles.FromString,
                )
        self.IsAuthorized = channel.unary_unary(
                '/gateway_backend.Auth/IsAuthorized',
                request_serializer=auth__pb2.Token.SerializeToString,
                response_deserializer=auth__pb2.IsValid.FromString,
                )


class AuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetPermissions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRoles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsAuthorized(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetPermissions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPermissions,
                    request_deserializer=auth__pb2.Token.FromString,
                    response_serializer=auth__pb2.Permissions.SerializeToString,
            ),
            'GetRoles': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRoles,
                    request_deserializer=auth__pb2.Token.FromString,
                    response_serializer=auth__pb2.Roles.SerializeToString,
            ),
            'IsAuthorized': grpc.unary_unary_rpc_method_handler(
                    servicer.IsAuthorized,
                    request_deserializer=auth__pb2.Token.FromString,
                    response_serializer=auth__pb2.IsValid.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gateway_backend.Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Auth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetPermissions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gateway_backend.Auth/GetPermissions',
            auth__pb2.Token.SerializeToString,
            auth__pb2.Permissions.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRoles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gateway_backend.Auth/GetRoles',
            auth__pb2.Token.SerializeToString,
            auth__pb2.Roles.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsAuthorized(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gateway_backend.Auth/IsAuthorized',
            auth__pb2.Token.SerializeToString,
            auth__pb2.IsValid.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
