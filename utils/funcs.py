import logging
import re
from datetime import timezone, datetime
from functools import lru_cache
from time import sleep
from typing import Any, Optional

import requests
from yarl import URL

import __init__
from utils.exeptions import InvalidUrl, GithubError
from utils.vars import footer_message, GITHUB_TOKEN, _MARKDOWN_STOCK_REGEX, _URL_REGEX

log = logging.getLogger(__name__)


def unlistify(lis: list) -> str:
    output = ""
    for i in lis:
        output += f"{i}   "
    return output


@lru_cache(maxsize=512)
def truncate(data: str, length: int, append: str = "") -> str:
    """
    Truncates a string to the given length\n
    `data` The string to truncate\n
    `length` The length to truncate to\n
    `append` Text to append to the end of truncated string. Default: ''
    """
    return (data[:length] + append) if len(data) + len(append) > length else data


@lru_cache(maxsize=512)
def alterLink(url: str) -> InvalidUrl | str:
    try:
        requests.get(url)
    except requests.exceptions.RequestException:
        return InvalidUrl("Url doesn't exist")
    if (
            url[:24] == "https://gist.github.com/"
            or url[:35] == "https://gist.githubusercontent.com/"
    ):
        if url[-4:] == ".txt" or url[-4:] == "/raw":
            pass
        else:
            url = f"{url}/raw"
    elif url[:21] == "https://pastebin.com/" in url:
        if "/raw" in url:
            pass
        else:
            index = url.find(".com") + 4
            url = url[:index] + "/raw" + url[index:]
    return url


@lru_cache(maxsize=512)
def getUrlText(url: str) -> str:
    uri = alterLink(url)
    response = requests.get(uri)
    data = response.text
    return data


def parse_ratelimit_header(request: Any, *, use_clock: bool = False) -> float:
    reset_after: Optional[str] = request.headers.get("X-Ratelimit-Reset-After")
    if use_clock or not reset_after:
        utc = timezone.utc
        now = datetime.now(utc)
        reset = datetime.fromtimestamp(float(request.headers["X-Ratelimit-Reset"]), utc)
        return (reset - now).total_seconds()
    else:
        return float(reset_after)


def github_request(method, url, *, params=None, data=None, headers=None):
    hdrs = {
        "Accept": "application/vnd.github.inertia-preview+json",
        "User-Agent": "Encodation ",
        "Authorization": f"token {GITHUB_TOKEN}",
    }

    req_url = URL("https://api.github.com") / url

    if headers is not None and isinstance(headers, dict):
        hdrs.update(headers)
    match method:
        case "POST":
            r = requests.post(req_url, params=params, json=data, headers=hdrs)
        case "GET":
            r = requests.get(req_url, params=params, json=data, headers=hdrs)
        case "PATCH":
            r = requests.patch(req_url, params=params, json=data, headers=hdrs)
        case _:
            return TypeError("invalid method type")
    remaining = r.headers.get("X-Ratelimit-Remaining")
    js = r.json()
    if r.status_code == 429 or remaining == "0":
        # wait before we release the lock
        delta = parse_ratelimit_header(r)
        sleep(delta)
        return github_request(method, url, params=params, data=data, headers=headers)
    elif 300 > r.status_code >= 200:
        return js
    else:
        raise GithubError(js["message"])


def create_gist(content, *, description=None, filename=None, public=True):
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }

    filename = filename or "output.txt"
    data = {"public": public, "files": {filename: {"content": content}}}

    if description:
        data["description"] = description

    js = github_request("POST", "gists", data=data, headers=headers)
    return js["html_url"]


@lru_cache(maxsize=512)
def remove_markdown(text: str, *, ignore_links: bool = True) -> str:
    """A helper function that removes markdown characters."""

    def replacement(match):
        groupdict = match.groupdict()
        return groupdict.get("url", "")

    regex = _MARKDOWN_STOCK_REGEX
    if ignore_links:
        regex = f"(?:{_URL_REGEX}|{regex})"
    return re.sub(regex, replacement, text, 0, re.MULTILINE)


def reply(message, content: str, nolog=False):
    try:
        if not nolog:
            log.info(
                f"Replying to message (id: {message.id}, author: {message.author}) content: {str(content)}"
            )
        message.reply(f"{content}" f"{footer_message()}")
    except Exception as e:
        log.error(f"REPLY FAILED: {e} @ {message.subreddit}")
        if str(e) == "403 Client Error: Forbidden":
            print("/r/" + message.subreddit + " has banned me.")
            log.critical("/r/" + message.subreddit + " has banned me.")
            __init__.Blacklist.add_subreddit(
                subreddit=message.subreddit, Reason="403 Error"
            )


def log_codec(message, codec: str):
    log.debug(f"{message.id} codec {codec} was chosen")


def log_codec_completion(message, codec_to: str, codec_from):
    log.debug(
        f"{message.id} The message has successfully been converted to {codec_to}, from {codec_from}"
    )


def send_help(message, parser):
    log.info(f"Sending Help to message (id: {message.id}, author: {message.author})")
    return reply(
        message,
        str(parser.format_help()).replace("usage: main.py", "Arguments"),
        nolog=True,
    )


def timeConverter(time: int):
    match time:
        case 1:
            return "1 am"
        case 2:
            return "2 am"
        case 3:
            return "3 am"
        case 4:
            return "4 am"
        case 5:
            return "5 am"
        case 6:
            return "6 am"
        case 7:
            return "7 am"
        case 8:
            return "8 am"
        case 9:
            return "9 am"
        case 10:
            return "10 am"
        case 11:
            return "11 am"
        case 12:
            return "12 pm"
        case 13:
            return "1 pm"
        case 14:
            return "2 pm"
        case 15:
            return "3 pm"
        case 16:
            return "4 pm"
        case 17:
            return "5 pm"
        case 18:
            return "6 pm"
        case 19:
            return "7 pm"
        case 20:
            return "8 pm"
        case 21:
            return "9 pm"
        case 22:
            return "10 pm"
        case 23:
            return "11 pm"
        case 0:
            return "12 am"
