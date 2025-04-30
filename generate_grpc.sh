#!/bin/bash

python -m grpc_tools.protoc \
  -Iproto \
  --python_out=producer/grpc \
  --grpc_python_out=producer/grpc \
  proto/student.proto