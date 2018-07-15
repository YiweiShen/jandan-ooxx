from bs4 import BeautifulSoup
from selenium import webdriver
import requests


URL_TEMP = 'http://jandan.net/ooxx/page-'


def download_pic(url_list):
    for url in url_list:
        r = requests.get(url)
        with open(str(url).split('/')[-1], 'wb') as f:
            f.write(r.content)


def get_total_page(START_URL='http://jandan.net/ooxx'):
    r = requests.get(START_URL)
    soup = BeautifulSoup(r.content, 'lxml')
    page_span = soup.findAll('span', {'class': 'current-comment-page'})[0]
    total_pages_num = int(page_span.get_text()[1:-1])
    return total_pages_num


def get_img_url_on_one_page(page_num):
    print('processing page ' + str(page_num))
    page_url = URL_TEMP + str(page_num)
    browser = webdriver.Chrome()
    browser.get(page_url)
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html, 'lxml')
    img_url_list = []
    for i in soup.findAll('a', {'class': 'view_img_link'}):
        img_url_list.append('http:' + str(i.get('href')))
    return img_url_list


if __name__ == '__main__':
    pages = get_total_page()
    print('total page number: ' + str(pages))
    for i in range(1, pages + 1):
        imgs = get_img_url_on_one_page(i)
        download_pic(imgs)
