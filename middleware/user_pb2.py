# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x04user\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\" \n\rLoginResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"3\n\rCreateRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\" \n\x0e\x43reateResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\x32z\n\x0bUserService\x12\x32\n\x05login\x12\x12.user.LoginRequest\x1a\x13.user.LoginResponse\"\x00\x12\x37\n\x08register\x12\x13.user.CreateRequest\x1a\x14.user.CreateResponse\"\x00\x62\x06proto3')



_LOGINREQUEST = DESCRIPTOR.message_types_by_name['LoginRequest']
_LOGINRESPONSE = DESCRIPTOR.message_types_by_name['LoginResponse']
_CREATEREQUEST = DESCRIPTOR.message_types_by_name['CreateRequest']
_CREATERESPONSE = DESCRIPTOR.message_types_by_name['CreateResponse']
LoginRequest = _reflection.GeneratedProtocolMessageType('LoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.LoginRequest)
  })
_sym_db.RegisterMessage(LoginRequest)

LoginResponse = _reflection.GeneratedProtocolMessageType('LoginResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOGINRESPONSE,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.LoginResponse)
  })
_sym_db.RegisterMessage(LoginResponse)

CreateRequest = _reflection.GeneratedProtocolMessageType('CreateRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.CreateRequest)
  })
_sym_db.RegisterMessage(CreateRequest)

CreateResponse = _reflection.GeneratedProtocolMessageType('CreateResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATERESPONSE,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.CreateResponse)
  })
_sym_db.RegisterMessage(CreateResponse)

_USERSERVICE = DESCRIPTOR.services_by_name['UserService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOGINREQUEST._serialized_start=20
  _LOGINREQUEST._serialized_end=70
  _LOGINRESPONSE._serialized_start=72
  _LOGINRESPONSE._serialized_end=104
  _CREATEREQUEST._serialized_start=106
  _CREATEREQUEST._serialized_end=157
  _CREATERESPONSE._serialized_start=159
  _CREATERESPONSE._serialized_end=191
  _USERSERVICE._serialized_start=193
  _USERSERVICE._serialized_end=315
# @@protoc_insertion_point(module_scope)
