import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def generate_answer(question, chunks):
    context = "\n\n".join(
        f"Source: {chunk.document.title}\n{chunk.content}"
        for chunk in chunks
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the "
                    "provided context. If the answer is not in "
                    "the context, say you don't know. "
                    "Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    return response.choices[0].message.content
