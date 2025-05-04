# importing the necessary libraries . . .
import grpc
import grpc_service.service_pb2 as service_pb2
import grpc_service.service_pb2_grpc as service_pb2_grpc

# client.py is just for manual testing, hardcoded a prompt here server is waiting for the input which it receives from the client.py and then it generates the image and saves it inside G disk . . .

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.Text2ImageServiceStub(channel)

    prompt = "A futuristic cyberpunk city at night"
    request = service_pb2.ImageRequest(prompt=prompt)

    response = stub.GenerateImage(request)
    print("Server response:", response.message)

if __name__ == '__main__':
    run()
