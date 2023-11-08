#!/usr/bin/python3
"""
This module contains a recursive function that queries the Reddit API,
parses the titles of hot articles, and prints a sorted count of given keywords
"""

import requests
import re


def count_words(subreddit, word_list, cont_dict={}, after=""):
    """
    Queries Reddit API, parses titles, and counts keywords.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count.
        count_dict (dict, optional): Dictionary to store counts. Defaults to
        after (str, optional): A token for pagination. Defaults to "".

    Returns:
        dict: Dictionary containing counts of keywords.
    """
    if subreddit is None:
        return None
    url = "http://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    user = {"User-Agent": "my_script:reddit_api:v1.0.0"}

    resp = requests.get(url, params={"after": after}, headers=user)

    if resp.status_code == 200:
        after = resp.json().get("data").get("after")
        if not after:
            cont_dict = sorted(cont_dict.items(), key=lambda x: (-x[1], x[0]))
            for word, occ in cont_dict:
                print('{}: {}'.format(word, occ))
            return
        for post in resp.json().get("data").get("children"):
            title = post.get("data").get("title").lower()
            for word in word_list:
                word = word.lower()
                if word in title:
                    cont_dict[word] = cont_dict.get(word, 0) + 1
        return count_words(subreddit, word_list, cont_dict, after)
