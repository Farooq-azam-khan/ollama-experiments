import ollama
# import asyncio


def chat(question: str, image: str):
    print("Running inferencing...")
    resp = ollama.generate(model="moondream", prompt=question, images=[image])
    return resp


if __name__ == "__main__":
    import pathlib

    image_dir = pathlib.Path("./demo-2-min.jpg")
    if image_dir.is_file():
        resp = chat(question="what do you see in this image?",
                    image=str(image_dir))
        pass
    else:
        print("image does not exist")
