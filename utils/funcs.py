import requests

from utils.exeptions import InvalidUrl


def truncate(data: str, length: int, append: str = '') -> str:
    """
    Truncates a string to the given length\n
    `data` The string to truncate\n
    `length` The length to truncate to\n
    `append` Text to append to the end of truncated string. Default: ''
    """
    return (data[:length] + append) if len(data) + len(append) > length else data


def alterLink(url: str) -> InvalidUrl | str:
    try:
        requests.get(url)
    except requests.exceptions.RequestException:
        return InvalidUrl("Url doesn't exist")
    if url[:24] == 'https://gist.github.com/' or url[:35] == 'https://gist.githubusercontent.com/':
        if url[-4:] == '.txt' or url[-4:] == '/raw':
            pass
        else:
            url = f'{url}/raw'
    elif url[:21] == 'https://pastebin.com/' in url:
        if '/raw' in url:
            pass
        else:
            index = url.find('.com') + 4
            url = url[:index] + '/raw' + url[index:]
    return url


def getUrlText(url: str) -> str:
    uri = alterLink(url)
    response = requests.get(uri)
    data = response.text
    print(data)
    return data
