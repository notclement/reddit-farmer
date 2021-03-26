#!/usr/bin/env python3

"""
s1_comment_scraper.py will run and save the best few comments into a file every few hours
Will overwrite the previous entries as long as the date is the same.
"""

import random

import sys
from praw import reddit
from secret_keys import *
from blacklist_words import blacklist
from replacement_mapping import dict_replacement
from datetime import datetime

TARGET_SUB = 'cryptocurrency'
sub = reddit.subreddit(TARGET_SUB).hot(limit=5)
COMMENT_LIMIT = 500
COMMENT_SORT_BY = 'best'
COMMENT_MAX_WORDS = 100
PATH = './comments/'
FILE = datetime.today().strftime('%d-%m-%Y-comments.txt')


def get_random_comment(arr):
    """Takes in array, returns 1 random item in the array"""
    randnum = random.randint(0, len(arr))
    return arr[randnum]


def return_filtered_comments(submission):
    """Takes in a submission object, returns a list of comments that are
    filtered based on blacklist, maxwords, top x comments"""
    submission.comment_sort = COMMENT_SORT_BY
    submission.comment_limit = COMMENT_LIMIT
    filtered_comments = []
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, praw.models.MoreComments):
            continue
        # Here you can fetch data off the comment.
        comment = top_level_comment.body

        # ensure that the comment does not contain any words in blacklist
        # and also it is less than COMMENT_MAX_WORDS
        fail_test = 0
        lcomment = comment.lower()
        for badword in blacklist:
            if badword not in lcomment and len(comment) < COMMENT_MAX_WORDS:
                pass
            else:
                fail_test += 1
        if not fail_test:
            filtered_comments.append(replace_words(comment).capitalize())

    return filtered_comments


def replace_words(comment):
    comment = comment.lower()
    for k, v in dict_replacement.items():
        if k in comment:
            rand_dict_entry = random.randint(1, len(dict_replacement[k])) - 1
            comment = comment.replace(k, dict_replacement[k][rand_dict_entry])
    return comment


def lst_to_file(comment_lst, fullpathname):
    with open(fullpathname, 'w') as writer:
        for comment in comment_lst:
            clean_raw_comment = repr(comment).lstrip('"\'').rstrip('"\'')
            writer.write(clean_raw_comment + '\n')


def get_daily_obj():
    daily_id = ''
    submissions = [x for x in sub if x.stickied]
    for submission in submissions:
        if 'daily' in submission.title.lower():
            # we will take the post id and write it to a file
            # then we will have the total number of files
            daily_id = submission
    return reddit.submission(id=daily_id)


def main():
    try:
        daily_obj = get_daily_obj()

        comment_lst = return_filtered_comments(daily_obj)
        len_comment_lst = len(comment_lst)
        fullpathname = PATH + FILE

        lst_to_file(comment_lst, fullpathname)

        print('{} comments added to {}'.format(len_comment_lst, fullpathname))
    except:
        sys.exit(0)


if __name__ == '__main__':
    main()
