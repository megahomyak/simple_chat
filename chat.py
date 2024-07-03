from groq import Groq
from pathlib import Path
import sys

here = Path(__file__).parent

with open(here / "groq_token.txt") as f:
    groq = Groq(api_key=f.read().strip())

chat_file_path = sys.argv[1]

with open(chat_file_path, encoding="utf-8") as f:
    chat_lines = f.read().rstrip().split("\n")

chat_messages = []
new_lines = []
for line in chat_lines:
    new_lines.append(line)
    role = None
    if line.startswith("USER "):
        line = line[5:] # Removing the "USER " part
        role = "user"
        chat_messages.append({
            "role": "user",
            "content": line,
        })
    elif line.startswith("ASSISTANT "):
        line = line[10:] # Removing the "ASSISTANT " part
        role = "assistant"
    elif line.startswith("SYSTEM "):
        line = line[7:] # Removing the "ASSISTANT " part
        role = "system"
    else:
        chat_messages[-1]["content"] += "\n" + line
    if role:
        chat_messages.append({
            "role": role,
            "content": line,
        })

completion = groq.chat.completions.create(
    model="llama3-70b-8192",
    messages=chat_messages,
)

response_lines = completion.choices[0].message.content.split("\n")
new_lines.append(f"ASSISTANT {response_lines[0]}")
for line in response_lines[1:]:
    new_lines.append(line)

with open(chat_file_path, "w", encoding="utf-8") as f:
    for line in new_lines:
        f.write(line + "\n")
