import logging
import re
from datetime import timezone, datetime
from time import sleep
from typing import Any, Optional

import requests
from yarl import URL

from utils.exeptions import InvalidUrl, GithubError
from utils.vars import footer_message, GITHUB_TOKEN, _MARKDOWN_STOCK_REGEX, _URL_REGEX

log = logging.getLogger(__name__)

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


def parse_ratelimit_header(request: Any, *, use_clock: bool = False) -> float:
    reset_after: Optional[str] = request.headers.get('X-Ratelimit-Reset-After')
    if use_clock or not reset_after:
        utc = timezone.utc
        now = datetime.now(utc)
        reset = datetime.fromtimestamp(float(request.headers['X-Ratelimit-Reset']), utc)
        return (reset - now).total_seconds()
    else:
        return float(reset_after)


def github_request(method, url, *, params=None, data=None, headers=None):
    hdrs = {
        'Accept': 'application/vnd.github.inertia-preview+json',
        'User-Agent': 'Encodation ',
        'Authorization': f'token {GITHUB_TOKEN}'
    }

    req_url = URL('https://api.github.com') / url

    if headers is not None and isinstance(headers, dict):
        hdrs.update(headers)
    match method:
        case 'POST':
            r = requests.post(req_url, params=params, json=data, headers=hdrs)
        case 'GET':
            r = requests.get(req_url, params=params, json=data, headers=hdrs)
        case 'PATCH':
            r = requests.patch(req_url, params=params, json=data, headers=hdrs)
        case _:
            return TypeError("invalid method type")
    remaining = r.headers.get('X-Ratelimit-Remaining')
    js = r.json()
    if r.status_code == 429 or remaining == '0':
        # wait before we release the lock
        delta = parse_ratelimit_header(r)
        sleep(delta)
        return github_request(method, url, params=params, data=data, headers=headers)
    elif 300 > r.status_code >= 200:
        return js
    else:
        raise GithubError(js['message'])


def create_gist(content, *, description=None, filename=None, public=True):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }

    filename = filename or 'output.txt'
    data = {
        'public': public,
        'files': {
            filename: {
                'content': content
            }
        }
    }

    if description:
        data['description'] = description

    js = github_request('POST', 'gists', data=data, headers=headers)
    return js['html_url']


def remove_markdown(text: str, *, ignore_links: bool = True) -> str:
    """A helper function that removes markdown characters.
    """

    def replacement(match):
        groupdict = match.groupdict()
        return groupdict.get('url', '')

    regex = _MARKDOWN_STOCK_REGEX
    if ignore_links:
        regex = f'(?:{_URL_REGEX}|{regex})'
    return re.sub(regex, replacement, text, 0, re.MULTILINE)

def reply(message, content: str):
    log.info(f'Replying to message (id: {message.id}, author: {message.author}) content: {str(content)}')
    message.reply(f'{content}'
                  f'{footer_message()}')
