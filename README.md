# Text2Image Microservice - Final Project

This project is a **Text-to-Image AI Agent** developed as part of the course requirement.  
It converts user prompts (text) into generated images using **Stable Diffusion v1.5**, running **locally**.

It is a fully working microservice with:
- **gRPC Server** (backend service)
- **FastAPI HTTP Bridge** (REST API wrapper)
- **Gradio Frontend** (user interface)
- **Postman Collection** for API testing
- **Docker-ready** (containerization setup coming)

---

# Project Architecture

          +----------------+
          |    Gradio App   | (http://127.0.0.1:7860)
          +--------+-------+
                   |
                   | HTTP POST /generate
                   |
          +--------v--------+
          |    FastAPI App   | (http://127.0.0.1:8000)
          |  (fastapi_bridge.py) |
          +--------+--------+
                   |
                   | gRPC request
                   |
          +--------v--------+
          |   gRPC Server    | (localhost:50051)
          |   (server.py)    |
          +--------+--------+
                   |
                   | Stable Diffusion model
                   |
          +--------v--------+
          |  Image Generated |
          |  and Saved on G:  |
          +------------------+

- FastAPI is acting like a translator between HTTP and gRPC.

- gRPC server is acting like the powerful image generator.

- Gradio/Postman are acting like the customers sending prompts.

# Setup Instructions

1. Clone the Repository

   - git clone https://github.com/ultimate144z/text2image-microservice.git
   - cd text2image-microservice

2. Install Requirements
   - pip install -r requirements.txt
   Or manually type:
   - pip install fastapi uvicorn gradio grpcio grpcio-tools diffusers transformers accelerate safetensors scipy

3. Running the Services

   - Make sure you go to the root directory first and ensure you have everything installed (from requirements.txt)
   - e.g root: C:\Users\HP\Desktop\fresh_test\Untitled Folder 13\ 
   - Also, make sure to open separate CMD terminals for each command below:
   
   - Run gRPC Server:
   - python -m grpc_service.server

   - Run FastAPI Bridge:
   - uvicorn fastapi_bridge:app --reload

   - Run Gradio Frontend:
   - python frontend_gradio.py
     
Make sure you have selected the correct Python version.

# Usage:

Access Gradio app at:
http://127.0.0.1:7860

Access FastAPI Swagger Docs at:
http://127.0.0.1:8000/docs

Test with Postman using the provided collection:
text2image_postman_collection.json

# Postman Collection:

So far we included three tests inside our postman collection:
- small prompt
- empty prompt
- big prompt

our raw JSON is essentially:
{
   "prompt": ""

}

 All tests POST to /generate endpoint.

```
text2image-microservice/
├── grpc_service/
│   ├── server.py
│   ├── client.py
│   ├── service_pb2.py
│   ├── service_pb2_grpc.py
│   ├── service.proto
├── model/
│   ├── generate_image.py
├── generate_image.ipynb
├── fastapi_bridge.py
├── frontend_gradio.py
├── text2image_postman_collection.json
├── Dockerfile (coming soon)
├── README.md
└── .gitignore
```

# Microservice Features

Features:
1. gRPC API Endpoint (GenerateImage) 
2. FastAPI REST Wrapper 
3. Async/Concurrent Handling 
4. Error Handling (invalid input) 
5. JSON Responses + Status Codes 
6. Gradio Frontend Interface 
7. Postman Testing Collection 
8. Docker Setup 

# Model Source

This project uses the following pre-trained model:

- [`runwayml/stable-diffusion-v1-5`](https://huggingface.co/runwayml/stable-diffusion-v1-5) from HuggingFace

Model weights are downloaded automatically at runtime. If the G:/ drive is unavailable, it defaults to local folder.

# Limitations

- Local CPU-only inference — image generation may be slow.
- No image customization controls yet (like style, seed, negative prompts).
- Not optimized for large-scale concurrent load.
- Requires internet to download the model the first time (unless already cached).

# Notes

- Models and generated images are saved locally in:
- G:/huggingface/generated_images/
- .env file is excluded from GitHub for security reasons.
- This project is developed for educational purposes only.

# Build the Docker image (just once)
docker build -t text2image-microservice .

# Run the app with required ports exposed
docker run -p 7860:7860 -p 8000:8000 -p 50051:50051 text2image-microservice

# Credits:
- Sarim Farooq | 22i-0458 | AI
- Musab Waseem | 22i-0488 | AI
