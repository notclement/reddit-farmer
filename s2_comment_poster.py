#!/usr/bin/env python3

"""
s2_comment_poster.py will post a random comment taken from the bulk comments from
the previous day
"""
import os
from functions import *


def main():
    if len(sys.argv) != 2:
        print('Program ended, need to give 1 arg to specify account to use')
        sys.exit(0)

    user = sys.argv[1]

    daily_obj = get_daily_obj(user)

    # This is mostly to check for first run, to create the common used file
    used_path = USED_PATH
    if not os.path.isfile(used_path):
        f = open(used_path, "w")
        f.write('')
        f.close()

    post_rand_comment(daily_obj)


if __name__ == '__main__':
    main()
