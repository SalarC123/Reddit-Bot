import praw
import re
from botsecrets import PUT_CLIENT_ID_HERE, PUT_CLIENT_SECRET_HERE, PUT_PASSWORD_HERE, PUT_USER_AGENT_HERE, PUT_USER_NAME_HERE
import time

reddit = praw.Reddit(client_id= PUT_CLIENT_ID_HERE,
                     client_secret= PUT_CLIENT_SECRET_HERE,
                     password= PUT_PASSWORD_HERE,
                     user_agent= PUT_USER_AGENT_HERE,
                     username= PUT_USER_NAME_HERE)

def anywordcountbot():
    while True:
        # Checks each comment in the generated stream of new comments
        # Skips bot calls that were made before the bot was running
        for comment in reddit.subreddit('all').stream.comments(skip_existing = True):
            try:
                # Checks for bot-name, username, word-to-check
                text = re.compile(r'anywordcountbot(\s)+(\w)+(\s)+(\w)+',re.I).search(comment.body).group()
            except:
                # Goes to next submission if word doesn't show up
                continue
            wordcount = 0
            # Divides comment into the bot-name, username, word-to-check
            commentattributes = text.split()
            try:
                # Checks each submission title and increases count for every instance
                for submission in reddit.redditor(commentattributes[1]).submissions.new(limit=None):
                    if commentattributes[2] in submission.title:
                        for word in submission.title.split():
                            if commentattributes[2].lower() == word.lower():
                                wordcount += 1
                    # Checks each submission text to increase count
                    if commentattributes[2] in submission.selftext:
                        for word in submission.selftext.split():
                            if commentattributes[2].lower() == word.lower():
                                wordcount += 1
                # Checks each comment and increases count for every instance
                for usercomment in reddit.redditor(commentattributes[1]).comments.new(limit=None):
                    if commentattributes[2] in usercomment.body:
                        for word in usercomment.body.split():
                            if commentattributes[2].lower() == word.lower():
                                wordcount += 1
            except:
                comment.reply(f'{commentattributes[1]} is not a real Reddit user!\n\nMake sure to omit the u/ and follow this format (letter case and spacing do not matter):\n\nanywordcountbot usertocheck  wordtocheck')
                continue
            # If the wordcount is one, times will not be plural ↓
            times = 'times'
            if wordcount == 1:
                times = times[:4]
            comment.reply(f'u/{commentattributes[1].title()} has said {commentattributes[2]} {wordcount} {times}')
            time.sleep(3)

anywordcountbot()
