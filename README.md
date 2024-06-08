# simple\_chat

"simple\_chat" is a simple program designed for chatting with LLMs through a text file.

## Usage

First, create a `groq_token.txt` file in the same directory where this README is and paste your Groq token into it.

Then, install all the dependencies from `pyproject.toml`. You can use `pip install dependency_name` for that, where `dependency_name` is the name of a dependency you see in `pyproject.toml`.

Then, run `python chat.py textfile`, where `textfile` is a path to a text file where your message history is stored. `chat.py` will append the assistant's response to the file. If the file does not exist, it will *not* be created. You have to create the file yourself.

## Chat file syntax

Each message starts with "ASSISTANT" or "USER" on a new line, then there is one space, then the message contents begin. Contents may be multiline: to make the next line part of message contents, begin it with ">" (no whitespace needed: it will be parsed as one with message contents, so don't add a whitespace for a pretty look)

### Example

```
USER Hello!
ASSISTANT Hello! How can I assist you today?
USER Today I want to write multiline
>
>text!
ASSISTANT That's great! Is there anything I can help with?
```
