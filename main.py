import asyncio
from tg_client import client, start_client, save_chat_history
from analyzer import run_analysis

async def main():
    await start_client()
    await save_chat_history()
    run_analysis()

if __name__ == "__main__":
    asyncio.run(main())
