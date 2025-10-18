import os, asyncio, websockets, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def interpret_task(natural_language):
    """Send the user's instruction to an LLM to translate it into structured browser actions."""
    prompt = f"""
    Convert this instruction into a simple JSON browser command:
    Examples:
      Input: 'Open Google and search for UI Agents'
      Output: {{"action": "search", "query": "UI Agents"}}
      Input: 'Go to https://huggingface.co'
      Output: {{"action": "open_tab", "url": "https://huggingface.co"}}
    Instruction: {natural_language}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except:
        return {"action": "search", "query": natural_language}

async def send_to_extension(cmd):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(cmd))
        print("Sent command:", cmd)

async def main():
    task = input("Enter your task: ")
    cmd = await interpret_task(task)
    await send_to_extension(cmd)

if __name__ == "__main__":
    asyncio.run(main())
