import requests
import random
import time

# Load API keys from file
with open('API.txt', 'r') as f:
    api_keys = [line.strip() for line in f if line.strip()]

# Load proxies from file
with open('proxy.txt', 'r') as f:
    proxies = [line.strip() for line in f if line.strip()]

# Load questions from file
with open('qs.txt', 'r') as f:
    questions = [line.strip() for line in f if line.strip()]

# Kiểm tra số lượng API và Proxy
if not api_keys or not proxies or not questions:
    print("Error: API.txt, proxy.txt hoặc qs.txt rỗng!")
    exit(1)

if len(api_keys) != len(proxies):
    print("Error: Số lượng API Key và Proxy không khớp!")
    exit(1)

URL = "https://api.hyperbolic.xyz/v1/chat/completions"

# Hàm kiểm tra IP của proxy
def check_ip(proxy):
    try:
        response = requests.get("https://api64.ipify.org?format=json", proxies={"http": proxy, "https": proxy}, timeout=10)
        ip = response.json().get("ip", "Unknown IP")
        print(f"Proxy {proxy} is using IP: {ip}")
    except Exception as e:
        print(f"Failed to check IP for proxy {proxy}: {e}")

# Hàm gửi request đến API
def send_chat_request(api_key, proxy, question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "messages": [{"role": "user", "content": question}],
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    proxies_dict = {"http": proxy, "https": proxy}

    try:
        response = requests.post(URL, headers=headers, json=data, proxies=proxies_dict, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
    except Exception as e:
        return f"Error: {e}"

# Hàm chạy bot
def run_chat_bot():
    while True:
        for api_key, proxy in zip(api_keys, proxies):
            question = random.choice(questions)
            print(f"\nUsing API Key: {api_key} with Proxy: {proxy}")
            check_ip(proxy)
            answer = send_chat_request(api_key, proxy, question)
            print(f"Question: {question}\nAnswer: {answer}")
            
            # Random delay between 60-120 seconds
            delay = random.uniform(60, 120)
            print(f"Waiting {delay:.1f} seconds before next question...")
            time.sleep(delay)

run_chat_bot()
