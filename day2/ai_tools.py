import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

SYSTEM_PROMPT = (
        "You are an assistant that analyzes the sentiment"
        "of the given text. Please respond with 'Good', "
        "'Bad', or 'Neutral' based on the sentiment."
    )

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze_sentiment(text):
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},

        ]
    )
    return response.choices[0].message.content


async def get_assistant_response(thread_id: str, message: str) -> str:
    await openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        content=message,
        role="user",
    )
    run = await openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=os.getenv("OPENAI_ASSISTANT_KEY")
    )
    while run.status != "completed":
        run = await openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    messages_paginator = openai_client.beta.threads.messages.list(thread_id=thread_id)
    async for message in messages_paginator:
        if message.role == "assistant":
            return message.content[0].text.value
    return "I'm sorry, I couldn't generate a response."
