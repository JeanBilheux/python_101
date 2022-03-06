import asyncio

async def main():
    print("Hello ...")
    await asyncio.sleep(2)
    print("   world!")
    
asyncio.run(main())
