# -*- coding: utf-8 -*-
from __future__ import print_function
import grpc
import random
from rpc.auth import auth_pb2
from rpc.auth import auth_pb2_grpc
from settings.base import configs

sso_rpc_servers = eval(configs.AUTH_RPC_SERVER)


def verifyToken(system_code: str = 'gatherone_crm', token: str = ''):
    channel = grpc.insecure_channel(random.choice(sso_rpc_servers))
    stub = auth_pb2_grpc.AuthServiceStub(channel)
    response = stub.VerifyToken(auth_pb2.VerifyTokenRequest(system_code=system_code, token=token))
    return response


if __name__ == '__main__':
    res = verifyToken('gatherone_crm',
                      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTY5MzUxMjksInVzZXJfaWQiOjUwLCJzZXNzaW9uX2lkIjoiZmRlY2IxMDEtNjA5Mi00Y2QxLWFhN2YtNjU3MjllOTdmNDg2In0.phgEu8lWCpCwBFMlCs_npydAKTEb54cXr3M3pYpHQX4')
