# coding:utf-8
import urllib
from requests import exceptions
from parsel import Selector


class VisitException(Exception):
    """website is unavailable"""
    pass


class ExtractException(Exception):
    """can't extract html label"""
    pass


def gen_encode_url(ytb_url='', domain=''):
    param_dict = {
        'url': ytb_url
    }
    param = urllib.parse.urlencode(param_dict)
    url = '{}?{}'.format(domain, param)
    return url


def urls_handler(session):
    op_download_sub_url = []
    playlist_url = []
    with open('pre_download_sub_url.txt') as urls:
        for url in urls:
            if 'playlist' in url:
                playlist_url.append(url.replace('\n', ''))
            else:
                print(url)
                op_download_sub_url.append(url.replace('\n', ''))

    for p_url in playlist_url:
        for url in get_urls_in_playlist(session, p_url):
            print(url)
            op_download_sub_url.append(url)

    with open('handled_url.txt', 'w') as f:
        for url in op_download_sub_url:
            f.write('{}\n'.format(url))


def get_post_args(session):
    """prepare data for http://www.downvids.net
to get videos url in playlist"""
    try:
        res = session.get(
            'http://www.downvids.net/download-youtube-playlist-videos',
            timeout=30,
        )
    except:
        raise VisitException('website is unavailable')
    selector = Selector(text=res.text)
    payload = {}
    try:
        payload['autoken'] = selector.xpath(
            "//form/input[@name='autoken']/@value"
        ).extract()[0]
        payload['authenticity_token'] = selector.xpath(
            "//form/input[@name='authenticity_token']/@value"
        ).extract()[0]
        payload['playlistok'] = selector.xpath(
            "//form/input[@name='playlistok']/@value"
        ).extract()[0]
        payload['hd'] = '2'  # ignore this. 1:default, 2:480p, 3:720p, 4:1080p
    except:
        raise ExtractException("can't extract html label")

    return payload


def get_urls_in_playlist(session, playlist_url=''):
    """get each url of videos in playlist"""
    try:
        payload = get_post_args(session)
        payload['playlist'] = playlist_url
    except:
        raise ExtractException('failed: extract playlist')

    res = session.post(
        "http://www.downvids.net/videoflv.php",
        data=payload,
    )
    selector = Selector(text=res.text)
    video_urls = selector.xpath(
        "//span[@class='thumb vcard author']/a/@href"
    ).extract()
    for url in video_urls:
        yield url


