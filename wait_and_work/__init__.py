import asyncio
from random import randint

async def main(input: str) -> str:
    time = randint(6, 10)
    await asyncio.sleep(time)  # Simula lavoro
    return f"Success "