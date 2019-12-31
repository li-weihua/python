import argparse
import os
import sys
import onnx_pb2

parser = argparse.ArgumentParser(
    description='generate the graph input and output tensor name.',
)

parser.add_argument('-i',
                    '--input',
                    type=str,
                    required=True,
                    help='an integer for the accumulator')


args = parser.parse_args()

if not os.path.isfile(args.input):
    print('{args.input} does not exit!')
    sys.exit(1)

modelproto = onnx_pb2.ModelProto()

with open(args.input, 'rb') as f:
   modelproto.ParseFromString(f.read())

# show basic model information!
print('model information:')
print(f'    model producer: {modelproto.producer_name}')
print(f'    producer version: {modelproto.producer_version}')
print(f'    domain: {modelproto.domain}')
print(f'    model version: {modelproto.model_version}')
print()

graph = modelproto.graph

output_nodes = []

for node in graph.output:
    output_nodes.append(node.name)

print(f'output nodes: {output_nodes}')

input_nodes_temp = []
init_nodes = []

for node in graph.input:
    input_nodes_temp.append(node.name)

for t in graph.initializer:
    init_nodes.append(t.name)

input_nodes = [item for item in input_nodes_temp if item not in init_nodes]

print(f'input nodes: {input_nodes}')

