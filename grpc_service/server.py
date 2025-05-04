# importing the necessary libraries . . .
from concurrent import futures
import grpc
import time
import os
import sys

# fallback logic to allow import of grpc_service.* from nested context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import grpc_service.service_pb2 as service_pb2
import grpc_service.service_pb2_grpc as service_pb2_grpc
from diffusers import StableDiffusionPipeline

# trying to use the G drive if available, fallback to current dir . . .
if os.path.exists("G:/huggingface"):
    hf_home = "G:/huggingface"
else:
    print("G drive not found. Using current directory for model cache.")
    hf_home = os.path.join(os.getcwd(), "huggingface")

# setting the required environment variables . . .
os.environ["HF_HOME"] = hf_home
os.environ["HUGGINGFACE_HUB_CACHE"] = os.path.join(hf_home, "hub_cache")
os.environ["TRANSFORMERS_CACHE"] = os.path.join(hf_home, "transformers")
os.environ["DIFFUSERS_CACHE"] = os.path.join(hf_home, "diffusers")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# ensuring that the cache directory exists . . .
os.makedirs(hf_home, exist_ok=True)

# Loading the model . . .
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    cache_dir=hf_home,
    use_safetensors=True
)
pipe = pipe.to("cpu")

# gRPC class and logic . . .
class Text2ImageService(service_pb2_grpc.Text2ImageServiceServicer):
    def GenerateImage(self, request, context):
        prompt = request.prompt
        
        if not prompt:
            return service_pb2.ImageResponse(message="Invalid prompt.")

        # Save path: <cache_dir>/generated_images/
        save_folder = os.path.join(hf_home, "generated_images")
        os.makedirs(save_folder, exist_ok=True)

        image = pipe(prompt, num_inference_steps=20, height=384, width=384).images[0]
        save_path = os.path.join(save_folder, f"{int(time.time())}.png")
        image.save(save_path)

        return service_pb2.ImageResponse(message=f"Image saved at {save_path}")

# gRPC server start logic
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    service_pb2_grpc.add_Text2ImageServiceServicer_to_server(Text2ImageService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server started on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
