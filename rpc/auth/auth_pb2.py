# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04\x61uth\"8\n\x12VerifyTokenRequest\x12\x13\n\x0bsystem_code\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"\x95\x02\n\x08UserData\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x0e\n\x06mobile\x18\x02 \x01(\t\x12\x11\n\treal_name\x18\x03 \x01(\t\x12\x12\n\navatar_url\x18\x04 \x01(\t\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12\x11\n\tis_active\x18\x06 \x01(\x05\x12\x14\n\x0cis_superuser\x18\x07 \x01(\x05\x12\x0f\n\x07\x62ind_wx\x18\x08 \x01(\x05\x12\x11\n\trole_name\x18\t \x01(\t\x12\x17\n\x0f\x64\x65partment_name\x18\n \x01(\t\x12\x13\n\x0bleader_name\x18\x0b \x01(\t\x12\x14\n\x0c\x63ompany_name\x18\x0c \x01(\t\x12\x0e\n\x06system\x18\r \x01(\t\x12\x11\n\tis_delete\x18\x0e \x01(\x05\"N\n\x13VerifyTokenResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x1c\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x0e.auth.UserData2J\n\x04\x41uth\x12\x42\n\x0bVerifyToken\x12\x18.auth.VerifyTokenRequest\x1a\x19.auth.VerifyTokenResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_VERIFYTOKENREQUEST']._serialized_start=20
  _globals['_VERIFYTOKENREQUEST']._serialized_end=76
  _globals['_USERDATA']._serialized_start=79
  _globals['_USERDATA']._serialized_end=356
  _globals['_VERIFYTOKENRESPONSE']._serialized_start=358
  _globals['_VERIFYTOKENRESPONSE']._serialized_end=436
  _globals['_AUTH']._serialized_start=438
  _globals['_AUTH']._serialized_end=512
# @@protoc_insertion_point(module_scope)
