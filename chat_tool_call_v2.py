import ollama
import asyncio


def get_current_weather(city: str):
    return f"{city} Weather: -10 deg C. 10km/hr 10% humidity. kinda cold ngl"


async def chat():
    model_name = "llama3.2:1b-instruct-fp16"
    chat_history = []
    chat_history.append({"role": "user", "content": "What is the weather in Toronto?"})
    response = ollama.chat(
        model=model_name,
        messages=chat_history,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The name of the city",
                            },
                        },
                        "required": ["city"],
                    },
                },
            },
        ],
    )
    for tool_call in response["message"]["tool_calls"]:
        print(f"{tool_call=}")
        if tool_call["function"]["name"] == "get_current_weather":
            resp = get_current_weather(city=tool_call["function"]["arguments"]["city"])
            print(f"{resp=}")
            chat_history.append({"role": "tool", "content": resp})

    print(f"{chat_history=}")
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)
    for s in stream:
        print(s["message"]["content"], end="", flush=True)


if __name__ == "__main__":
    asyncio.run(chat())
