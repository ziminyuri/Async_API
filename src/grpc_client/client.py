from typing import Optional

import grpc

from grpc_client.stubs import auth_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub: Optional[auth_pb2_grpc.AuthStub] = None


async def get_stub() -> auth_pb2_grpc.AuthStub:
    return stub
