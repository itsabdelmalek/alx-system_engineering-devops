#!/usr/bin/python3

"""
This module contains a recursive function that queries the Reddit API,
parses the titles of hot articles, and prints a sorted count of given keywords.
"""

import requests

def count_words(subreddit, word_list, count_dict={}, after=""):
    """
    Queries Reddit API, parses titles, and counts keywords.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count.
        count_dict (dict, optional): Dictionary to store counts. Defaults to {}.
        after (str, optional): A token for pagination. Defaults to "".

    Returns:
        dict: Dictionary containing counts of keywords.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    headers = {
        "User-Agent": "my_script:reddit_api:v1.0.0 (by /u/Nickname-Pending1)"
    }
    params = {
        "after": after,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code == 404:
        return count_dict

    data = response.json().get("data")
    after = data.get("after")
    for child in data.get("children"):
        title = child.get("data").get("title").lower()
        for word in word_list:
            if title.count(word.lower()) > 0:
                count_dict[word.lower()] = count_dict.get(word.lower(), 0) + title.count(word.lower())

    if after is not None:
        return count_words(subreddit, word_list, count_dict, after)
    return count_dict

if __name__ == "__main__":
    subreddit_name = "learnpython"  # Replace with the subreddit you want to check
    keywords = ["python", "java", "javascript", "cpp", "c#"]  # Replace with your list of keywords
    count_dict = count_words(subreddit_name, keywords)
    if count_dict:
        sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for keyword, count in sorted_counts:
            print(f"{keyword}: {count}")
    else:
        print("No posts match or the subreddit is invalid.")
