import platform
import re
import time

import config as c
import logger as log
import praw


def testMain():
    i = 0
    #    enforceTitle()
    while 1:
        try:
            # checkFlairs is a fully functional Flair-Enforcer. It's currently disabled because no subreddit I moderate
            # requires me to host one of these.
            # checkFlairs(reddit=reddit, subreddit=subreddit)
            
            # Update all required files
            
            for item in subreddit.new():
                # Update Sidebar links to Megathreads
                print(item)
            
            print("-----")


        except ConnectionResetError:
            log.connectionError("ConnectionResetError")
            time.sleep(30)
        except ConnectionRefusedError:
            log.connectionError("ConnectionRefusedError")
            time.sleep(30)
        except ConnectionAbortedError:
            log.connectionError("ConnectionAbortedError")
            time.sleep(30)
        except ConnectionError:
            log.connectionError("ConnectionError")
            time.sleep(30)
        except Exception as e:
            log.unhandledException(exception=e, location="botCore.main()")
            time.sleep(30)
        time.sleep(c.BOT_CYCLE_TIME)


# Initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    reddit = praw.Reddit(client_id=c.BOT_LOGIN_CLIENT_ID, client_secret=c.BOT_LOGIN_SECRET, username=c.BOT_LOGIN_NAME,
                         password=c.BOT_LOGIN_PASSWORD, user_agent=c.BOT_USER_AGENT)
    subreddit = reddit.subreddit(c.BOT_SUBREDDIT_TO_MONITOR)
    moderator = subreddit.mod
    if platform.system() == "Windows":
        testMain()
