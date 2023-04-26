# -*- coding: utf-8 -*-
"""Get GitHub traffic data for a repository"""

import os

import requests


def naturalise(n: int) -> str:
    """Convert a number to human-readable string. E.g. 3200 -> "3.2K"

    :param n: int: Integer number
    :return: str: Human-readable string
    """

    if n < 1000:           # 123     -> "123" 
        n = str(n)
    elif n < 999_499:      # 1234    -> "1.2K"
        n = f'{n/1000:.3g}K'
    elif n < 999_999_499:  # 1234567 -> "1.23M"
        n = f'{n/1_000_000:.3g}M'
    return n


def naturalise_date(d: str) -> str:
    """Convert a datetime string to year-month format.
    E.g. '2023-04-25T00:18:30Z' -> Apr 2023

    :param n: int: Integer number
    :return: str: Human-readable string
    """

    # Numeric month to English month map
    month_str = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                 '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    year = d[0:4]
    month = month_str[d[5:7]]
    return month + ' ' + year


def get_traffic(repo: str) -> dict:
    """Get traffic data for a repository.

    :param repo: str: The repository name
    :return: dict: {views: int, clones: int, last_commit: datetime}
    """

    # Get the #. of views
    url = f'https://api.github.com/repos/{repo}/traffic/views'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {TOKEN}',
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    n_views = data['count']

    # Get the #. of clones
    url = f'https://api.github.com/repos/{repo}/traffic/clones'
    resp = requests.get(url, headers=headers)
    data = resp.json()
    n_clones = data['count']

    # Get the last commit date
    url = f'https://api.github.com/repos/{repo}/commits'
    resp = requests.get(url, headers=headers)
    data = resp.json()
    last_commit = data[0]['commit']['author']['date']
    return {'views': naturalise(n_views),
            'clones': naturalise(n_clones),
            'last_commit': naturalise_date(last_commit)}


if __name__ == '__main__':
    # Get traffic data for the repository
    TOKEN = os.environ['TOKEN']
    traffic = get_traffic('harningle/StataEditor')

    # Gen. svg badge
    working_dir = 'docs/assets/images'
    os.makedirs(working_dir, exist_ok=True)
    os.system(f'badge views {traffic["views"]} :brightgreen > {working_dir}/views.svg')
    os.system(f'badge clones {traffic["clones"]} :brightgreen > {working_dir}/clones.svg')
    os.system(
        f'''badge "last commit" "{traffic['last_commit']}" :blue > {working_dir}/last_commit.svg'''
    )
