import praw, time, re
import flairEnforcer as flair
import config as c
import unitReport as ur


# Probation Bot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def updateBannedUsers(subreddit):
    c.giveaway_banned_users.clear()
    page = subreddit.wiki['mods/giveawaybans']
    list = page.content_md.split(';')
    for name in list:
        c.giveaway_banned_users.append(name.strip())
        if name == '':
            c.giveaway_banned_users.remove(name)
    print(c.giveaway_banned_users)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Controllers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def initiateUnitReportCheck(comment):
    if comment.id not in c.checked_comments:
        if "!unit " in comment.body and comment.author == "lolTerryP":
            regex = re.findall('!unit (\d+)', comment.body)
            output = ""
            i = 0
            for number in regex:
                if i > 2:
                    break
                output += ur.buildReport(number)
                i += 1
            output += c.MESSAGE_FOOTER
            comment.reply(output)
            print("Replied to " + comment.permalink(fast=True))
        c.checked_comments.append(comment.id)


def checkFlairs(reddit, subreddit):
    # FlairEnforcer
    try:
        flair.checkNewSubmissions(subreddit=subreddit, approved_submissions=c.approved_submissions,
                                  submissions_with_no_flair=c.submissions_with_no_flair)
    except Exception as e:
        print(">>> Unhandled exception occured: " + str(type(e)))
    
    try:
        flair.revisitSubmissions(reddit=reddit, approved_submissions=c.approved_submissions,
                                 submissions_with_no_flair=c.submissions_with_no_flair,
                                 removed_submissions=c.removed_submissions, id_for_replies=c.id_for_replies)
    except Exception as e:
        print(">>> Unhandled exception occured: " + str(type(e)))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
reddit = praw.Reddit(client_id=c.BOT_LOGIN_CLIENT_ID, client_secret=c.BOT_LOGIN_SECRET, username=c.BOT_LOGIN_NAME,
                     password=c.BOT_LOGIN_PASSWORD, user_agent=c.BOT_USER_AGENT)
subreddit = reddit.subreddit(c.BOT_SUBREDDIT_TO_MONITOR)
i = 0

while 1:
    # checkFlairs(reddit=reddit, subreddit=subreddit)
    updateBannedUsers(subreddit)
    
    
    for comment in subreddit.comments(limit=5):
        # UnitReporter
        initiateUnitReportCheck(comment)
        if " Weekly Updated Giveaway Megathread" in comment.submission.title:
            print(comment.id + " ::: in GA thread")
        print(comment.id)

    # UnitReporter Update
    if i == 0:
        #updateBannedUsers(subreddit)
        ur.updateFiles()
    elif i == 1000:
        updateBannedUsers(subreddit)
        ur.updateFiles()
        i = 1
    i += 1
    
    time.sleep(c.BOT_CYCLE_TIME)
