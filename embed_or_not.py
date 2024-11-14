import asyncio
import ollama
from tqdm import tqdm

print("Reading Book...")


def get_book():
    book = ""
    with open("crime and punishment.txt") as f:
        book = f.read()
        return book


book = get_book()


def organize_book(book):
    parts = ["\n\n\nPART " + part for part in book.split("\n\n\nPART ")]
    chapters_by_part = [
        ["\n\n\nCHAPTER " + chapter for chapter in part.split("\n\n\nCHAPTER ")]
        for part in parts
    ]
    return chapters_by_part


def embed_organized_book(organized_book):
    print("Embedding Text...")
    # preface_embeds = ollama.embed(model="nomic-embed-text", prompt=preface)
    chapters_by_part_embeds = []
    for chs in tqdm(organized_book):
        chs_embeds = []
        for ch in chs:
            chs_embeds.append(ollama.embeddings(model="nomic-embed-text", prompt=ch))
        chapters_by_part_embeds.append(chs_embeds)
    return chapters_by_part_embeds


async def chat(question: str, context: str):
    print("Running inferencing...")
    async for token in await ollama.AsyncClient().chat(
        model="llama3.2:1b-instruct-fp16",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": """
Help me understand russian literature, but only use the context I provide. 
Limit yoursel to ten sentences.
""".strip()
            },
            {
                "role": "user",
                "content": f"# Context\n{context}\n\n# Question\n{question}",
            },
        ],
    ):
        print(token["message"]["content"], flush=True, end="")


if __name__ == "__main__":
    book = get_book()
    organized_book = organize_book(book)

    # 1. How does the book start? 
    # 2. who is the main character?
    # 3. List the characters here.
    # 4. What is the setting throughout the chapter?
    question = input(">> ")
    asyncio.run(chat(question=question, context=organized_book[1][1]))
