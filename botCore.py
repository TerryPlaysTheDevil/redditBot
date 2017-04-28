import praw, time, re
import flairEnforcer as flair, config as c, unitReport as ur, logger as log, probation as prob


# Controllers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def initiateUnitReportCheck(comment):
    try:
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
                log.unitReported(comment.permalink(fast=True))
            c.checked_comments.append(comment.id)
    except Exception as e:
        log.unhandledException(exception=e, location="botCore.initiateUnitReportCheck()")

def checkFlairs(reddit, subreddit):
    # FlairEnforcer
    try:
        flair.checkNewSubmissions(subreddit=subreddit, approved_submissions=c.approved_submissions,
                                  submissions_with_no_flair=c.submissions_with_no_flair, self="")
    except Exception as e:
        log.unhandledException(exception=e, location="botCore.checkFlairs()_newSubmissions")
    
    try:
        flair.revisitSubmissions(reddit=reddit, approved_submissions=c.approved_submissions,
                                 submissions_with_no_flair=c.submissions_with_no_flair,
                                 removed_submissions=c.removed_submissions, id_for_replies=c.id_for_replies, self="")
    except Exception as e:
        log.unhandledException(exception=e, location="botCore.checkFlairs()_oldSubmissions")


# Initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
reddit = praw.Reddit(client_id=c.BOT_LOGIN_CLIENT_ID, client_secret=c.BOT_LOGIN_SECRET, username=c.BOT_LOGIN_NAME,
                     password=c.BOT_LOGIN_PASSWORD, user_agent=c.BOT_USER_AGENT)
subreddit = reddit.subreddit(c.BOT_SUBREDDIT_TO_MONITOR)
i = 0


while 1:
    try:
        ### checkFlairs is a fully functional Flair-Enforcer. It's currently disabled because no subreddit I moderate
        #  requires me to host one of these.
        # checkFlairs(reddit=reddit, subreddit=subreddit)
        
        # Update all required files
        if i == 0:
            prob.updateBannedUsers(subreddit)
            ur.updateFiles()
        elif i == 100:
            prob.updateBannedUsers(subreddit)
            ur.updateFiles()
            i = 1
       
        for comment in subreddit.comments(limit=5):
            # UnitReporter
            initiateUnitReportCheck(comment)
            if comment.author in c.giveaway_banned_users:
                prob.probationControl(comment)
    except ConnectionResetError:
        time.sleep(30)
    except ConnectionRefusedError:
        time.sleep(30)
    except ConnectionAbortedError:
        time.sleep(30)
    except ConnectionError:
        time.sleep(30)
    except Exception as e:
        log.unhandledException(exception=e, location="botCore.main()")
    i += 1
    time.sleep(c.BOT_CYCLE_TIME)
