# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: largeimage.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='largeimage.proto',
  package='LargeImageProc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x10largeimage.proto\x12\x0eLargeImageProc\"\x19\n\x08OneImage\x12\r\n\x05image\x18\x01 \x01(\x0c\"\x18\n\x06Status\x12\x0e\n\x06status\x18\x01 \x01(\x08\x32O\n\x0bTransferRPC\x12@\n\x08Transfer\x12\x18.LargeImageProc.OneImage\x1a\x16.LargeImageProc.Status\"\x00(\x01\x62\x06proto3')
)




_ONEIMAGE = _descriptor.Descriptor(
  name='OneImage',
  full_name='LargeImageProc.OneImage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='LargeImageProc.OneImage.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=36,
  serialized_end=61,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='LargeImageProc.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='LargeImageProc.Status.status', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=63,
  serialized_end=87,
)

DESCRIPTOR.message_types_by_name['OneImage'] = _ONEIMAGE
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OneImage = _reflection.GeneratedProtocolMessageType('OneImage', (_message.Message,), {
  'DESCRIPTOR' : _ONEIMAGE,
  '__module__' : 'largeimage_pb2'
  # @@protoc_insertion_point(class_scope:LargeImageProc.OneImage)
  })
_sym_db.RegisterMessage(OneImage)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'largeimage_pb2'
  # @@protoc_insertion_point(class_scope:LargeImageProc.Status)
  })
_sym_db.RegisterMessage(Status)



_TRANSFERRPC = _descriptor.ServiceDescriptor(
  name='TransferRPC',
  full_name='LargeImageProc.TransferRPC',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=89,
  serialized_end=168,
  methods=[
  _descriptor.MethodDescriptor(
    name='Transfer',
    full_name='LargeImageProc.TransferRPC.Transfer',
    index=0,
    containing_service=None,
    input_type=_ONEIMAGE,
    output_type=_STATUS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRANSFERRPC)

DESCRIPTOR.services_by_name['TransferRPC'] = _TRANSFERRPC

# @@protoc_insertion_point(module_scope)
