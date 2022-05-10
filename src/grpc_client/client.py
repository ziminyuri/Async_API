from typing import Optional

import grpc

from core import config
from grpc_client.stubs import auth_pb2_grpc
from helpers import get_credentials

client_key, client_cert, ca_cert = get_credentials()
client_creds = grpc.ssl_channel_credentials(root_certificates=ca_cert,
                                            private_key=client_key,
                                            certificate_chain=client_cert)
channel = grpc.aio.secure_channel(f'{config.GRPC_HOST}:{config.GRPC_PORT}',
                                  client_creds)

stub: Optional[auth_pb2_grpc.AuthStub] = None


async def get_stub() -> auth_pb2_grpc.AuthStub:
    return stub
