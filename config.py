# Configuration Section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BOT_SUBREDDIT_TO_MONITOR = "OnePieceTC"  # Add more than one like so: "Subreddit_1+Subreddit_2+Subreddit_3"
BOT_LOGIN_NAME = "XXX"
BOT_LOGIN_PASSWORD = "YYY"
BOT_LOGIN_CLIENT_ID = "ZZZ"
BOT_LOGIN_SECRET = "WASD"

BOT_USER_AGENT = "USERAGENT"
BOT_CYCLE_TIME = 5  # How long do you want the bot to sleep after every run. Be aware that each cycle takes about 5
# seconds to complete, so a 5 second cycle pause would mean a completed run about every 10 seconds

# Message Footer
MESSAGE_FOOTER = "\n\n-----\n**[Please read this.](/str)** I am a bot in development by /u/lolTerryP. If you have a " \
                 "suggestion or a question, feel free to PM" \
                 " him by clicking [here](https://www.reddit.com/message/compose?to=lolTerryP&subject=OPTCBot)."



# Flair Enforcer
SUBMISSION_FETCH_LIMIT = 10
FLAIR_TIME_LIMIT = 1020  # If you change this, change it in the FLAIR_FLAIR_MISSING_MESSAGE as well
FLAIR_FIRST_GRACE_PERIOD = 120  # Needs to be smaller than FLAIR_TIME_LIMIT
FLAIR_FLAIR_MISSING_MESSAGE_DEFAULT = ""
FLAIR_FLAIR_MISSING_MESSAGE_OPTC = ("/r/OnePieceTC requires you to flair your post!\n\n"
                                    "This post has been automatically removed but will be re-approved (*and this "
                                    "comment deleted*) once a flair has been set.\n\n"
                                    "Please refer to [this guideline](/r/OnePieceTC/wiki/linkflairs) on how to "
                                    "properly set the right flair.\n\n"
                                    "**You do not need to delete or re-submit your post!**\n\n"
                                    "\n\nPlease be aware that this submission will only be monitored for 15 minutes "
                                    "after this comment was created. If you add a flair after that, it will have no "
                                    "effect "
                                    "and you will have to resubmit your post.\n\n")

FLAIR_FLAIR_MISSING_MESSAGE_NARUTO = ""


def decideSubreddit(subreddit):
    if subreddit == "OnePieceTC":
        return FLAIR_FLAIR_MISSING_MESSAGE_OPTC
    elif subreddit == "NarutoBlazing":
        return FLAIR_FLAIR_MISSING_MESSAGE_NARUTO
        # elif subreddit == "XXX":
        #    return (FLAIR_FLAIR_MISSING_MESSAGE_XXX)
    else:
        # subreddit could not be identified for some reason, eg trouble with the API, I'd recommend to have a default
        #  message for this situation
        return FLAIR_FLAIR_MISSING_MESSAGE_DEFAULT

