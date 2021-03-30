#!/usr/bin/env python3

"""
s1_comment_scraper.py will run and save the best few comments into a file every few hours
Will overwrite the previous entries as long as the date is the same.
"""

from functions import *
import sys


def main():
    try:
        daily_obj = get_daily_obj()
        comment_lst = return_filtered_comments(daily_obj)
        len_comment_lst = len(comment_lst)

        today_obj = get_todays_date_obj(daily_obj)
        full_filepath_today = get_file_path(today_obj)

        lst_to_file(comment_lst, full_filepath_today)

        print('{} comments added to {}'.format(len_comment_lst,
                                               full_filepath_today))
    except:
        sys.exit(0)


if __name__ == '__main__':
    main()
