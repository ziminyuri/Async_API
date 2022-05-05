from typing import Optional

import grpc

from core import config
from grpc_client.stubs import auth_pb2_grpc

channel = grpc.aio.insecure_channel(f'{config.GRPC_HOST}:{config.GRPC_PORT}')
stub: Optional[auth_pb2_grpc.AuthStub] = None


async def get_stub() -> auth_pb2_grpc.AuthStub:
    return stub
