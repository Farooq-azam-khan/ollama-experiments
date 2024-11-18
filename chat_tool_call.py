import ollama
import asyncio


async def chat():
    model_name = "llama3.2:1b-instruct-fp16"
    python_tag = "<|python_tag|>"
    run_python = False
    chat_history = [
        {
            "role": "system",
            "content": "Environment: ipython\nTools: brave_search",
        },
        {
            "role": "user",
            "content": "Can you search up the top news articles on hacker news and the new york times. Compare them as well.",
        },
    ]

    response = ollama.chat(model=model_name, messages=chat_history)
    chat_history.append(
        {"role": "assistant", "content": response["message"]["content"]}
    )
    chat_history.append(
        {
            "role": "tool",
            "content": "1. (nytimes.com) Np/=P solved. Nobel prize immanent.\n\n2. (news.ycombinator.com) all of physics has been solve. who knew it was so easy",
        }
    )
    print(chat_history)
    async for token in await ollama.AsyncClient().chat(
        model=model_name, messages=chat_history, stream=True, tools=[]
    ):
        token_str = token["message"]["content"]
        print(token_str, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(chat())
