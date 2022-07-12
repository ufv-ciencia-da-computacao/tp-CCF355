#!/bin/bash

python3 -m grpc_tools.protoc -I./middleware/protos --python_out=./middleware --grpc_python_out=./middleware ./middleware/protos/*.proto