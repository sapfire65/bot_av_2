from bs4 import BeautifulSoup
import requests
from random import randint


URL = 'https://www.useragents.me/'
defoult_user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36'}

def random_ua() -> str:
    """Парсит актуальный агенты и возвращает рандомный"""

    my_set = set()
    responce = requests.get(URL, headers=defoult_user_agent).text
    soup = BeautifulSoup(responce, 'lxml')
    textarea = soup.find_all('textarea', {'class': "form-control ua-textarea"})

    for i in textarea:
        my_set.add(i.text)

    random_agent = list(my_set)
    random_count = randint(1, len(random_agent))

    random_agent = list(my_set)[random_count]
    return random_agent



