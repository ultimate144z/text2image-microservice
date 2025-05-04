# importing the necessary libraries . . .
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc
import grpc_service.service_pb2 as service_pb2
import grpc_service.service_pb2_grpc as service_pb2_grpc

app = FastAPI()

# now defining the input format using Pydantic . . .
class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate") # single endpoint . . .

# function to make the image . . .
def generate_image(request: PromptRequest):
    try:
        # trying to connect to gRPC server . . .
        channel = grpc.insecure_channel('localhost:50051')
        stub = service_pb2_grpc.Text2ImageServiceStub(channel)

        # now making a request . . .
        grpc_request = service_pb2.ImageRequest(prompt=request.prompt)

        # and now calling the gRPC server . . .
        response = stub.GenerateImage(grpc_request)

        return {
            "status": "success",
            "message": response.message
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))