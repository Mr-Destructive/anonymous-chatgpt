# Anonymous ChatGPT Client 

- Access basic ChatGPT model without authentication

OpenAI recently made the ChatGPT model accessible anonymously. You can access it without authentication.
Read more about it in the [official docs](https://openai.com/blog/start-using-chatgpt-instantly)

## Installation

- Install the package/cli

```bash
pip install anonymous-chatgpt
```

## Usage

### CLI

```bash
chatgpt --prompt "hello world"
```

#### CLI Demonstration

![Anonymous ChatGPT Demo](https://meetgor-cdn.pages.dev/anonymous-chatgpt-demo.gif)

### Package

```bash
from anonymous_chatgpt import chat


message = chat(prompt="hello world")
print(message)
```


## Process of creating a authentication-less client

1. Send the first request to the ChatGPT API i.e. `chat.openai.com`
2. The response of that request has cookies for authentication(not user just user-agent and csrf tokens)
3. Those cookies are carried in all the upcoming requests
4. Send the second request to the [Sential API](https://techcommunity.microsoft.com/t5/manufacturing/introduction-to-openai-and-microsoft-sentinel/ba-p/3761907) i.e. `/backend-anon/sentinel/chat-requirements`
5. This request gives us the `sentinel-token` which is the token used for authentication and authorization of the requests (not users).
6. We use this token in all the subsequent requests
7. The third request is the actual request to the **Anonymous Conversation** endpoint i.e. `/backend-anon/conversation`
8. This is a streamed request which returns the response in the form of chunks

