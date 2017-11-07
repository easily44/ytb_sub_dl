# coding: utf-8
from requests import Session, exceptions
from parsel import Selector
from utils import gen_encode_url, urls_handler


def subtitle(session, ytb_url='', file_path=''):
    domain = 'http://downsub.com/'
    s_url = gen_encode_url(ytb_url, domain)
    # print(s_url)

    try:
        res = session.get(s_url, timeout=3)
    except exceptions.ReadTimeout:
        return 'url', s_url
    selector = Selector(text=res.text)
    abs_url = selector.xpath(
        "//div[@id='show']/b[1]/a/@href"
    ).extract()[0]
    download_url = domain + abs_url[2:]
    title = selector.xpath(
        "//span[@class='media-heading']/text()"
    ).extract()[0]
    print(download_url)  # todo: 到时换成log方式
    try:
        res = session.get(download_url, timeout=3)
    except exceptions.ReadTimeout:
        return 'download_url', download_url
    with open('{}/{}.srt'.format(file_path, title), 'w') as srt:
        srt.write(res.text)


if __name__ == '__main__':
    # 待下载ytb的url
    # todo: 看看到时转成settings.py的方式，然后这里用python的命令行解析包解析cmd参数
    # url = 'https://www.youtube.com/watch?v=Vyp5_F42NGs'
    filepath = '/Users/zhangyue/Downloads'
    # proxy = 'socks5://127.0.0.1:1080'
    proxy = None
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/60.0.3112.90 Safari/537.36',
        'connection': 'keep-alive',
    }
    session = Session()
    session.headers = headers
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        session.proxies = proxies

    urls_handler(session)

    urls_list = []
    with open('handled_url.txt') as f:
        for url in f:
            if url:
                urls_list.append(url)
    for i in urls_list:
        subtitle(session, i, filepath)


