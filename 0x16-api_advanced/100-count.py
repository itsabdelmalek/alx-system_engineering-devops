#!/usr/bin/python3
"""
This module contains a recursive function that queries the Reddit API,
parses the titles of hot articles, and prints a sorted count of given keywords
"""
import requests


def count_words(subreddit, word_list, wo_count=None, after=None):
    """
    Queries Reddit API, parses titles, and counts keywords.
    """
    if wo_count is None:
        wo_count = {}
    if subreddit is None or type(subreddit) is not str:
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "reddit_api:v1.0.0 (by /u/Nickname-Pending1)"}

    params = {"after": after}

    resp = requests.get(url, headers=headers,
                        params=params, allow_redirects=False)
    if resp.status_code == 200:
        data = resp.json()
        children = data["data"]["children"]

        for child in children:
            title = child["data"]["title"].lower()

            for word in word_list:
                word = word.lower()

                if word in title:
                    wo_count[word] = wo_count.get(word, 0) + 1

        after = data["data"]["after"]
        if after:
            return count_words(subreddit, word_list, wo_count, after)
        else:
            sorted_word_count = sorted(wo_count.items(),
                                       key=lambda x: (-x[1], x[0]))
            for word, count in sorted_word_count:
                print(f"{word}: {count}")
            return
    elif resp.status_code == 404:
        return
    else:
        return
