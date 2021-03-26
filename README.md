# reddit farmer
 
## What it does

- Uses Reddit API to scrape comments from dailies and add it to a text file
- Grab random comments from the text files saved in the previous day to post
- Get moons
 
## To use
1. Populate ```secret_keys.py``` with your reddit api details
2. Set up cronjob to run ```s1_comment_scraper.py``` every few hours
3. Set up cronjob to run ```s2_comment_poster``` every few hours
 