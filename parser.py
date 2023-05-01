from requests import Session
from re import findall

headers = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Cache-Control': 'max-age=0', 
    'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'}

session = Session()

def parse_channel_link(request):
    response = session.get(f'https://www.youtube.com/results?search_query={request}', headers=headers).text

    return str(findall(r'\/\@.+', response)[0]).split(',')[0][:-1]


def get_videos(channel_link, videos_quantity):
    videos_page_link = 'https://www.youtube.com/' + channel_link + '/videos'
    response = session.get(videos_page_link, headers=headers).text

    link_location = list(filter(lambda x: len(x.split('v=')[1]) > 5, search_for_link_location(response)))

    return link_location[:videos_quantity]


def search_for_link_location(response):
    start = response.find('ytInitialData')
    link_location = response[start + 17:]
    end = link_location.find('}};')
    link_location = link_location[:end] + '}}'

    return list(map(lambda x: 'https://www.youtube.com' + x, findall(r'(?<="url":")\/\w+\?v=\w+', link_location)))


def main(request, videos_quantity):    
    channel_link = parse_channel_link(request)
    videos = get_videos(channel_link, videos_quantity)

    return videos
