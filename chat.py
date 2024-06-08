from groq import Groq
from pathlib import Path
import sys

here = Path(__file__).parent

with open(here / "groq_token.txt") as f:
    groq = Groq(api_key=f.read().strip())

chat_file_path = sys.argv[1]

with open(chat_file_path, encoding="utf-8") as f:
    chat_lines = f.readlines()

chat_messages = []
for line in chat_lines:
    if line.startswith("USER "):
        line = line[5:] # Removing the "USER " part
        chat_messages.append({
            "role": "user",
            "message": line,
        })
    elif line.startswith("ASSISTANT "):
        line = line[10:] # Removing the "ASSISTANT " part
        chat_messages.append({
            "role": "assistant",
            "message": line,
        })
    elif line.startswith(">"):
        line = line[1:] # Removing the ">" character
        chat_messages[-1]["message"] += "\n" + line

completion = groq.chat.completions.create(
    model="llama3-70b-8192",
    messages=chat_messages,
)

response_lines = completion.choices[0].message.content.split("\n")
with open(chat_file_path, encoding="utf-8") as f:
    f.write(f"\nASSISTANT {response_lines[0]}")
    for line in response_lines[1:]:
        f.write(f"\n>{line}")
