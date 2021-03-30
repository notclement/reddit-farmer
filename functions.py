import sys
import random
import requests
import json
from datetime import datetime, timedelta
from secret_keys import *
from blacklist_words import blacklist
from replacement_mapping import dict_replacement

TARGET_SUB = 'cryptocurrency'
sub = reddit1.subreddit(TARGET_SUB).hot(limit=5)
COMMENT_LIMIT = 5000
COMMENT_SORT_BY = 'best'
COMMENT_MAX_WORDS = 200
PATH = './comments/'
USED_PATH = './comments/used-comments.txt'

# ======= global info for api (keys) =======
API_URL = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"
API_HEADER_HOST = 'x-rapidapi-host'
API_ENDP = 'rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com'
API_HEADER_APIKEY = 'x-rapidapi-key'
API_BODY_LANG_K = 'language'
API_BODY_STRENGTH_K = 'strength'
API_BODY_COMMENT_K = 'text'
API_BODY_LANG_V = 'en'
API_BODY_STRENGTH_V = 3
# ==========================================


def append_used_comment_to_file(comment):
    """Take in a comment and append it to the used file"""
    path = USED_PATH
    with open(path, 'a+') as fp:
        fp.write(repr(comment).lstrip('"\'').rstrip('"\'') + '\n')


def comment_used(comment):
    """check if a comment has been used, if so, return false"""
    path = USED_PATH
    all_comments = read_from_file_into_lst(path)
    if comment in all_comments:
        return True
    else:
        return False


def post_rand_comment(obj, counter=0):
    """Post a random comment but not before rephrasing and used checks"""
    used_path = USED_PATH
    full_filepath_yesterday = get_file_path(get_yesterdays_date_obj(obj))
    lst_comment = read_from_file_into_lst(full_filepath_yesterday)
    comment = get_random_comment(lst_comment)

    if comment not in read_from_file_into_lst(used_path):
        if not comment_used(comment):
            print('============ copied comments ============')
            comment = replace_words(comment)
            print(comment)
            print('=========== rephrased comment ===========')
            rephrased_comment = rephrase(comment)
            print(replace_words(rephrased_comment))
            print('=========================================')

            # randomly rephrase or not
            if random.randint(0, 0):
                # this is live, dont anyhow spam this
                obj.reply(replace_words(comment))
                print('Posted without paraphrase.')
            else:
                # this is live, dont anyhow spam this
                obj.reply(replace_words(rephrased_comment))
                print('Posted with paraphrase.')

            append_used_comment_to_file(comment)

            print('Comment posted and added to the used file')
    else:
        if counter > len(read_from_file_into_lst(used_path)) * 15:
            print('All comments have been used. Bye.')
            sys.exit(0)
        post_rand_comment(obj, counter + 1)


def get_file_path(obj):
    """Take in an object and returns the filepath to it"""
    return PATH + obj.strftime('%d-%B-%Y-comments.txt')


def get_todays_date_obj(obj):
    """Get the date of the daily post and return the date
    in %d-%B-%Y format"""
    title = obj.title
    daily_title = title.split(' ')
    todays_date = '{}-{}-{}'.format(daily_title[4].rstrip(','),
                                    daily_title[3], daily_title[5])
    todays_date = datetime.strptime(todays_date, '%d-%B-%Y')
    return todays_date


def get_yesterdays_date_obj(obj):
    return get_todays_date_obj(obj) - timedelta(1)


def rephrase(comment):
    """Use the rephrase api to rephrased comment"""
    payload = {
        API_BODY_LANG_K: API_BODY_LANG_V,
        API_BODY_STRENGTH_K: API_BODY_STRENGTH_V,
        API_BODY_COMMENT_K: comment
    }
    payload = json.dumps(payload)
    headers = {
        'content-type': "application/json",
        API_HEADER_APIKEY: rephrase_api_key,
        API_HEADER_HOST: API_ENDP
    }
    response = requests.request("POST", API_URL, data=payload, headers=headers)
    rephrased = json.loads(response.text)
    return rephrased["rewrite"]


def read_from_file_into_lst(filepath):
    """Reading from file into a list and return the list"""
    lst = []
    with open(filepath) as fp:
        for line in fp:
            lst.append(line.strip())
    return lst


def get_random_comment(arr):
    """Takes in array, returns 1 random item in the array"""
    try:
        randnum = random.randint(0, len(arr) - 1)
        return arr[randnum]
    except IndexError:
        randnum = random.randint(0, 50)
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
    """Use the replacement_mapping file as a guide to replace words and
    return the comment with capitalisation"""
    comment = comment.lower()
    for k, v in dict_replacement.items():
        if k in comment:
            rand_dict_entry = random.randint(0, len(dict_replacement[k]) - 1)
            comment = comment.replace(k, dict_replacement[k][rand_dict_entry])
    return comment.capitalize()


def lst_to_file(comment_lst, fullpathname):
    """Write an incoming list into a file"""
    with open(fullpathname, 'w') as writer:
        for comment in comment_lst:
            clean_raw_comment = repr(comment).lstrip('"\'').rstrip('"\'')
            writer.write(clean_raw_comment + '\n')


def get_daily_obj(user='1'):
    """Get the reddit obj of the input user"""
    daily_id = ''
    submissions = [x for x in sub if x.stickied]
    for submission in submissions:
        if 'daily' in submission.title.lower():
            # we will take the post id and write it to a file
            # then we will have the total number of files
            daily_id = submission
    if user == '1':
        return reddit1.submission(id=daily_id)
    elif user == '2':
        return reddit2.submission(id=daily_id)


def main():
    pass


if __name__ == '__main__':
    main()
