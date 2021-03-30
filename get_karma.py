from functions import *
from secret_keys import *


def get_prev_run_karma(user):
    filepath = './karma_scores/{}.txt'.format(user)
    with open(filepath, 'r') as reader:
        karma = reader.readlines()
    return int(karma[0])


def save_prev_run(user, comment_karma):
    filepath = './karma_scores/{}.txt'.format(user)
    with open(filepath, 'w+') as writer:
        writer.write(str(comment_karma))


def get_comment_karma(user):
    user_obj = reddit1.redditor(user)
    comment_karma = user_obj.comment_karma
    return comment_karma


def get_difference(old_num, new_num):
    if new_num >= old_num:
        return '+{}'.format(abs(new_num - old_num))
    else:
        return '-{}'.format(abs(new_num - old_num))


def print_deets(user, curr_karma):
    prev_karma = get_prev_run_karma(user)
    difference = get_difference(prev_karma, curr_karma)
    save_prev_run(user, curr_karma)
    print('{} -> {} ({})'.format(user, curr_karma, difference))


def main():
    print('Comment Karma:')
    u_user1 = 'ItzChiips'
    u_user2 = 'sarif3210'
    print_deets(u_user1, get_comment_karma(u_user1))
    print_deets(u_user2, get_comment_karma(u_user2))


if __name__ == '__main__':
    main()
