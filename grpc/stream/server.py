from concurrent import futures
import time
import logging

import grpc

import largeimage_pb2
import largeimage_pb2_grpc

import numpy as np

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class TransferRPC(largeimage_pb2_grpc.TransferRPCServicer):

    def Transfer(self, request_iterator, context):

        t1 = time.perf_counter()
        image = b''
        for chunk in request_iterator: 
            image += chunk.image

        #print(len(image))

        t2 = time.perf_counter()
        print((t2-t1)*1000)
        return largeimage_pb2.Status(status = True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    largeimage_pb2_grpc.add_TransferRPCServicer_to_server(TransferRPC(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('server started, listen 50051')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
