import argparse
import requests
import json
import uuid


BASE_URL = "https://chat.openai.com"


def prepare_chat_request():

    # First request to get the cookies
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    request_client = requests.session()
    response = request_client.get(BASE_URL, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    set_cookie = response.cookies.get_dict()

    cookies = "; ".join([f"{key}={value}" for key, value in set_cookie.items()])

    chat_req_url = f"{BASE_URL}/backend-anon/sentinel/chat-requirements"
    headers = {
        "accept": "text/event-stream",
        "accept-language": "en-GB,en;q=0.8",
        "content-type": "application/json",
        "cookie": cookies,
        "oai-device-id": set_cookie.get("oai-did"),
        "oai-language": "en-US",
        "origin": "https://chat.openai.com",
        "referer": "https://chat.openai.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    # second request to get the OpenAI's Sentinel token
    chat_req_res = request_client.post(chat_req_url, headers=headers)
    chat_req_token = ""
    if chat_req_res.status_code == 200:
        chat_req_token = chat_req_res.json().get("token")
        headers = {
            **headers,
            "openai-sentinel-chat-requirements-token": chat_req_token,
        }
    else:
        chat_req_res.raise_for_status()
    return request_client, headers


def chat_prompt(prompt: str):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    resp_message = {}

    # first request to get the cookies
    request_client, headers = prepare_chat_request()

    # third request to get the response to the prompt
    url = f"{BASE_URL}/backend-anon/conversation"

    parent_id = str(uuid.uuid4())
    msg_id = str(uuid.uuid4())

    data = {
        "action": "next",
        "messages": [
            {
                "id": f"{msg_id}",
                "author": {"role": "user"},
                "content": {"content_type": "text", "parts": [f"{prompt}"]},
                "metadata": {},
            }
        ],
        "parent_message_id": f"{parent_id}",
        "model": "text-davinci-002-render-sha",
        "timezone_offset_min": -330,
        "history_and_training_disabled": True,
        "conversation_mode": {"kind": "primary_assistant"},
        "force_paragen": False,
        "force_paragen_model_slug": "",
        "force_nulligen": False,
        "force_rate_limit": False,
    }

    response = request_client.post(url, headers=headers, json=data)
    if response.status_code != 200:
        resp_message["error"] = response.text
        response.raise_for_status()
    data = response.text
    msgs = data.split("\ndata:")
    if len(msgs) > 1:
        resp = json.loads(msgs[-2])
        messages = resp.get("message", {}).get("content", {}).get("parts", [])
        if len(messages) > 0:
            resp_message["message"] = messages[0]
    return resp_message


def chat():
    parent_id = str(uuid.uuid4())
    msg_id = str(uuid.uuid4())
    prompt = input("user >> ")
    data = {
        "action": "next",
        "messages": [
            {
                "id": f"{msg_id}",
                "author": {"role": "user"},
                "content": {"content_type": "text", "parts": [f"{prompt}"]},
                "metadata": {},
            }
        ],
        "parent_message_id": f"{parent_id}",
        "model": "text-davinci-002-render-sha",
        "timezone_offset_min": -330,
        "history_and_training_disabled": True,
        "conversation_mode": {"kind": "primary_assistant"},
        "force_paragen": False,
        "force_paragen_model_slug": "",
        "force_nulligen": False,
        "force_rate_limit": False,
    }
    while True:
        data["messages"].append(
            {
                "id": str(uuid.uuid4()),
                "author": {"role": "user"},
                "content": {"content_type": "text", "parts": [f"{prompt}"]},
                "metadata": {},
            }
        )
        request_client, headers = prepare_chat_request()
        url = f"{BASE_URL}/backend-anon/conversation"

        response = request_client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            response.raise_for_status()
        resp = response.text
        msgs = resp.split("\ndata:")
        if len(msgs) > 1:
            resp = json.loads(msgs[-2])
            messages = resp.get("message", {}).get("content", {}).get("parts", [])
            if len(messages) > 0:
                print("bot >> ", messages[0])
                data.get("messages",[]).append(
                    {
                        "id": str(uuid.uuid4()),
                        "author": {"role": "assistant"},
                        "content": {"content_type": "text", "parts": [messages[0]]},
                        "metadata": {},
                    }
                )
            prompt = input("user >> ")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--prompt", type=str)
    args.add_argument("--chat", action="store_true")
    args = args.parse_args()
    prompt = args.prompt
    if args.chat:
        chat()
    else:
        response = chat_prompt(prompt)
        print(response)

if __name__ == "__main__":
    main()
