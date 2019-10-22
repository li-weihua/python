all: largeimage_pb2.py  largeimage_pb2_grpc.py

largeimage_pb2.py largeimage_pb2_grpc.py: largeimage.proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. largeimage.proto

.PHONY: all
