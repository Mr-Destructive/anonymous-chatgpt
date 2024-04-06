import argparse
import requests
import json
import uuid


def simple_chat():
    BASE_URL = "https://chat.openai.com"

    args = argparse.ArgumentParser()
    args.add_argument("--prompt", type=str, required=True)
    args = args.parse_args()

    prompt = args.prompt

    # First request to get the cookies
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    request_client = requests.session()
    response = request_client.get(BASE_URL, headers=headers)
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


    # third request to get the response to the prompt
    url = f"{BASE_URL}/backend-anon/conversation"
    headers = {
        **headers,
        "openai-sentinel-chat-requirements-token": chat_req_token,
    }

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
        print(response.status_code, response.text)
        return
    data = response.text
    msgs = data.split("\ndata:")
    if len(msgs) > 1:
        resp = json.loads(msgs[-2])
        print(resp["message"]["content"]["parts"][0])

def main():
    simple_chat()

if __name__ == "__main__":
    main()

