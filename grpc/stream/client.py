import logging
import time

import grpc

import largeimage_pb2
import largeimage_pb2_grpc

import numpy as np

def generate_imgiter(imgstr):
    chunks = len(imgstr)
    chunk_size = 3*1024*1024 # 1M
    for i in range(0, chunks, chunk_size):
        yield largeimage_pb2.OneImage(image=imgstr[i:i+chunk_size])

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = largeimage_pb2_grpc.TransferRPCStub(channel)

        x = np.ones([8*1024*1024], dtype=np.uint8)

        img_iter = generate_imgiter(x.tostring())

        t1 = time.perf_counter()
        response = stub.Transfer(img_iter)
        t2 = time.perf_counter()

        print((t2-t1)*1000)
        #print(response.status)


if __name__ == '__main__':
    logging.basicConfig()
    run()

