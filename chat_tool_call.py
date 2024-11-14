import ollama
import asyncio


async def chat():
    run_python = False
    async for token in await ollama.AsyncClient().chat(
        model="llama3.2:1b-instruct-fp16",
        messages=[
            {
                "role": "system",
                "content": "Environment: ipython\nTools: brave_search",
            },
            {"role": "user", "content": "Can you search up the top news articles on hacker news and the new york times. Compare them as well."},
        ],
        stream=True,
    ):
        if token["message"]["content"] == "<|python_tag|>":
            run_python = True
            print("---> execute <---")
        else:
            print(token["message"]["content"], end="", flush=True)
        if token["done"]:
            print()
            print("total duration:", token["total_duration"] // 1000)
            if run_python:
                print("-----------")


asyncio.run(chat())
