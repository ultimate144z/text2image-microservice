import multiprocessing
import subprocess

def run_fastapi():
    subprocess.run(["python", "fastapi_bridge.py"])

def run_gradio():
    subprocess.run(["python", "frontend_gradio.py"])

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_fastapi)
    p2 = multiprocessing.Process(target=run_gradio)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
