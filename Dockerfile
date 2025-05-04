# 🐍 Use an official lightweight Python image
FROM python:3.10-slim

# 🏗️ Set working directory inside container
WORKDIR /app

# 🌍 Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/huggingface
ENV TRANSFORMERS_CACHE=/app/huggingface/transformers
ENV DIFFUSERS_CACHE=/app/huggingface/diffusers

# 🧽 Create huggingface directories
RUN mkdir -p /app/huggingface/generated_images

# 📋 Copy all project files into the container
COPY . .

# 🛠️ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🚪 Expose needed ports
EXPOSE 50051 8000 7860

# 🚀 Start FastAPI + Gradio together
CMD ["python", "start_services.py"]
