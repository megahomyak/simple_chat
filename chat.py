from groq import Groq
from pathlib import Path
import sys

here = Path(__file__).parent

with open(here / "groq_token.txt") as f:
    groq = Groq(api_key=f.read().strip())

chat_file_path = sys.argv[1]
try:
    check_rejections = sys.argv[2] == "y"
except IndexError:
    check_rejections = False

with open(chat_file_path, encoding="utf-8") as f:
    chat_lines = f.read().rstrip().split("\n")

temperature = 0

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
        line = line[len("ASSISTANT "):]
        role = "assistant"
    elif line.startswith("TEMPERATURE "):
        temperature = float(line[len("TEMPERATURE "):])
        continue
    elif line.startswith("SYSTEM "):
        line = line[len("SYSTEM "):]
        role = "system"
    else:
        chat_messages[-1]["content"] += "\n" + line
    if role:
        chat_messages.append({
            "role": role,
            "content": line,
        })

def is_rejection(text):
    completion = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": f'"""\n{text}\n"""\n\nDoes the message in triple quotes look like a rejection to create a response? Respond with "YES" or "NO" (without quotes)'
            }
        ],
    )
    response = completion.choices[0].message.content
    if response == "YES":
        print(f"REJECTED: {text}")
        return True
    return False

while True:
    completion = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_messages,
        temperature=temperature,
    )
    response = completion.choices[0].message.content
    if not is_rejection(response):
        break

response_lines = response.split("\n")
new_lines.append(f"ASSISTANT {response_lines[0]}")
for line in response_lines[1:]:
    new_lines.append(line)

with open(chat_file_path, "w", encoding="utf-8") as f:
    for line in new_lines:
        f.write(line + "\n")
