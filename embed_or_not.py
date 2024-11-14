import asyncio
import ollama

print("Reading Book...")
book = ""
with open("crime and punishment.txt") as f:
    book = f.read()

preface = book[: book.find("CHAPTER I")]
chapter1 = book[book.find("CHAPTER I") : book.find("CHAPTER II")][:1000]

print("Embedding Text...")
# preface_embeds = ollama.embed(model="nomic-embed-text", prompt=preface)
# chapter1_embeds = ollama.embeddings(model="nomic-embed-text", prompt=chapter1)
# print(f'{len(chapter1_embeds)}')


async def chat():
    print("Running inferencing...")
    async for token in await ollama.AsyncClient().chat(
        model="llama3.2:1b-instruct-fp16",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": "Help me understand russian literature, but only use the context I provide. Limit yoursel to ten sentences.",
            },
            {
                "role": "user",
                "content": f"# Context\n{chapter1}\n\n# Question\n How does this book start?",
            },
        ],
    ):
        print(token["message"]['content'], flush=True, end="")


asyncio.run(chat())
