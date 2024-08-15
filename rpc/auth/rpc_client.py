# -*- coding: utf-8 -*-
from __future__ import print_function
import grpc
from core.customer_consul import CustomerConsul
from rpc.auth import auth_pb2_grpc, auth_pb2


def verifyToken(system_code: str = 'gatherone_ucenter', token: str = ''):
    my_consul = CustomerConsul()
    server_host, server_port = my_consul.discover_service('ucenter')
    channel = grpc.insecure_channel(f'{server_host}:{server_port}')
    # channel = grpc.insecure_channel('172.18.134.227:50052')
    stub = auth_pb2_grpc.AuthStub(channel)
    response = stub.VerifyToken(auth_pb2.VerifyTokenRequest(system_code=system_code, token=token))
    return response


if __name__ == '__main__':
    res = verifyToken('gatherone_crm',
                      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTY5MzUxMjksInVzZXJfaWQiOjUwLCJzZXNzaW9uX2lkIjoiZmRlY2IxMDEtNjA5Mi00Y2QxLWFhN2YtNjU3MjllOTdmNDg2In0.phgEu8lWCpCwBFMlCs_npydAKTEb54cXr3M3pYpHQX4')
    print(res)
