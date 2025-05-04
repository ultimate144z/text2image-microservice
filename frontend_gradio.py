# importing the necessary libraries . . .
import gradio as gr
import requests

# making the function that generates the image via a prompt . . .
def generate_image(prompt):
    
    try:
        # simply sending the POST request to FastAPI server . . .
        response = requests.post(
            "http://127.0.0.1:8000/generate",
            json={"prompt": prompt}
        )
        
        # indicating success . . .
        if response.status_code == 200:
            message = response.json()["message"]
            return f"Success!\n{message}"
        
            # failure . . .
        else:
            return f"Failed with status code: {response.status_code}\n{response.json()}"
        
    except Exception as e:
        return f"Error: {str(e)}"

# now making the Gradio UI . . .
iface = gr.Interface(
    fn=generate_image,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
    title="Text-to-Image Generator",
    description="Enter a prompt to generate an image using the AI backend."
)

if __name__ == "__main__":
    iface.launch()