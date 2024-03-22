import asyncio
import logging
from generators import Generator
import httpx

async def run_generator(generator_id: int):
    generator = Generator(generator_id)
    
    async with httpx.AsyncClient() as client:
        while True:
            data = generator.generate_data()
            try:
                response = await client.post("http://localhost:8000/generator_data/", json=data.dict())
                response.raise_for_status()
                print(f"Generator {generator_id}: Data sent successfully.")
            except httpx.HTTPError as e:
                print(f"Generator {generator_id}: An error occurred while sending data: {e}")
            await asyncio.sleep(60)  # Espera antes de generar nuevos datos

async def main():
    generator_tasks = [run_generator(i) for i in range(10)]
    await asyncio.gather(*generator_tasks)

if __name__ == "__main__":
    asyncio.run(main())