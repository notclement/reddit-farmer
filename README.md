# Reddit Moons Farmer
 
## What it does
- Uses Reddit API to scrape comments from /r/Cryptocurrency daily and add it to a text file
- Grab random comments from the previous day and paraphrase it before posting
- Keep track of comments that are posted
- Get moons
 
## Automating the Process of Posting Comments
1. Populate ```secret_keys.py``` with your paraphrase and reddit api details
2. Create ```./comments``` and ```./karma_scores``` folders
3. Set up cronjob to run ```s1_comment_scraper.py``` every x hours
4. Set up cronjob to run ```s2_comment_poster.py``` every x hours
 
## Tracking Karma Gained / Lost
Change the reddit usernames in ```get_karma.py``` and run to see the karma change since the script last ran
 
## APIs Used
- Python Reddit API Wrapper (https://praw.readthedocs.io/en/latest/)
- Paraphrase API (https://rapidapi.com/smodin/api/rewriter-paraphraser-text-changer-multi-language)

## Good to have
1. Add in sentiment checker (post only positive comments)
3. AI ChatBot reply to people who comment on our comment

## WARNING
USE AT YOUR OWN RISK. 

BOTTING IS A BANNABLE OFFENCE.

YOU SHOULD NOT BOT THE COMMENTS AS IT DEFEATS THE PURPOSE OF A COMMUNITY DRIVEN FORUM.

## LICENSE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The version that generates comments that are indistinguishable from normal comment will not be released.

Want to collaborate? Let's get in touch.
