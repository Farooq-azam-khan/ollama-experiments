import ollama
import asyncio


def chat(question: str, image: str):
    import base64

    with open(image, "rb") as image_raw:
        print("reading base64 image")
        image_base64 = base64.b64encode(image_raw.read()).decode("utf-8")
        print("Running inferencing...")
        resp = ollama.chat(
            model="moondream",
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "images": [image_base64],
                }
            ],
        )
        return resp


if __name__ == "__main__":
    import pathlib

    image_dir = pathlib.Path("./mbappe - messi world cup 2022 heat map.jpg")
    if image_dir.is_file():
        resp = chat(
            question="what do you see in this image?",
            image=str(image_dir),
        )
    else:
        print("image does not exist")
