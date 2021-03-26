#!/usr/bin/env python3

"""
s2_comment_poster.py will post a random comment taken from the bulk comments from
the previous day
"""

from custom_comments import custom_comments
from s1_comment_scraper import *
from datetime import datetime, timedelta


def read_from_file_into_lst(filepath):
    lst = []
    with open(filepath) as fp:
        for line in fp:
            lst.append(line.strip())
    return lst


def main():
    yesterday = datetime.now() - timedelta(1)
    yesterday = yesterday.strftime('%d-%m-%Y-comments.txt')
    filepath_yesterday = PATH + yesterday
    lst_comment = read_from_file_into_lst(filepath_yesterday)

    # ========= get 1 rando comment ===========
    # if not 0, get from post comments
    if random.randint(0, 2):
        print('============ copied comments ============')
        comment = get_random_comment(lst_comment)
    # if 0, will get from custom comments
    else:
        print('============ custom comments ============')
        comment = get_random_comment(custom_comments)

    print(comment)
    print('=========================================')
    # ==========================================

    # # post live, don't spam this mate
    get_daily_obj().reply(replace_words(comment).capitalize())


if __name__ == '__main__':
    main()
