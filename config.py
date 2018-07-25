import platform

# Configuration Section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if platform.system() == "Linux":
    BOT_SUBREDDIT_TO_MONITOR = "OnePieceTC"
elif platform.system() == "Windows":
    BOT_SUBREDDIT_TO_MONITOR = "OnePieceTC"  # Add more than one like so: "Subreddit_1+Subreddit_2+Subreddit_3"
BOT_LOGIN_NAME = "OPTCBot"
BOT_LOGIN_PASSWORD = redacted
BOT_LOGIN_CLIENT_ID = redacted
BOT_LOGIN_SECRET = redacted

BOT_USER_AGENT = "Subreddit monitoring and moderation bot with some subreddit specific functionalities for " \
                 "/r/OnePieceTC by /u/lolTerryP"
BOT_CYCLE_TIME = 5  # How long do you want the bot to sleep after every run. Be aware that each cycle takes about 5
# seconds to complete, so a 5 second cycle pause would mean a completed run about every 10 seconds

SUB_MODERATORS = []

# Message Footer
if platform.system() == "Windows":
    MESSAGE_FOOTER = "\n\n-----\n**[Please read this.](/str)** I am a bot in development by /u/lolTerryP. If you have a " \
                     "suggestion or a question, feel free to PM him by clicking [here](" \
                     "https://www.reddit.com/message/compose?to=lolTerryP&subject=OPTCBot). \n\n This is a TEST version of the bot!"
else:
    MESSAGE_FOOTER = "\n\n-----\n**[Please read this.](/str)** I am a bot in development by /u/lolTerryP. If you have a" \
                     " suggestion or a question, feel free to PM him by clicking [here](" \
                     "https://www.reddit.com/message/compose?to=lolTerryP&subject=OPTCBot)."

# File directories ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if platform.system() == "Linux":
    unitsPath = "/bin/redditBot/files/units.json"
    unitsPathTemp = "/bin/redditBot/files/units_temp.json"
    detailsPath = "/bin/redditBot/files/details.json"
    detailsPathTemp = "/bin/redditBot/files/details_temp.json"
    cdPath = "/bin/redditBot/files/cooldowns.json"
    cdPathTemp = "/bin/redditBot/files/cooldowns_temp.json"
    logFile = "/bin/redditBot/files/log.txt"
elif platform.system() == "Windows":
    unitsPath = "C:/redditBot/units.json"
    unitsPathTemp = "C:/redditBot/units_temp.json"
    detailsPath = "C:/redditBot/details.json"
    detailsPathTemp = "C:/redditBot/details_temp.json"
    cdPath = "C:/redditBot/cooldowns.json"
    cdPathTemp = "C:/redditBot/cooldowns_temp.json"
    logFile = "C:/redditBot/log.txt"

# Probation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
giveaway_banned_users = []
giveaway_ban_message_title = 'You have been permanently banned from /r/OnePieceTC'
giveaway_ban_message_1 = 'Hello '
giveaway_ban_message_2 = ',\n\nbecause of previous misbehavior the moderators of /r/OnePieceTC have placed you on ' \
                         'probation. You have violated the rules of this agreement by submitting another comment to ' \
                         'the GiveAway thread. Because of this, you have been banned from the subreddit permanently. ' \
                         '\n\n ' \
                         'If you want to appeal the ban, please send a modmail to the moderators of /r/OnePiece. '
giveaway_handled = []

# Flair Enforcer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
approved_submissions = []
submissions_with_no_flair = []
removed_submissions = []
ur_checked_comments = []
t_checked_comments = []
id_for_replies = {}
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
        return (FLAIR_FLAIR_MISSING_MESSAGE_OPTC)
    elif subreddit == "NarutoBlazing":
        return (FLAIR_FLAIR_MISSING_MESSAGE_NARUTO)
        # elif subreddit == "XXX":
        #    return (FLAIR_FLAIR_MISSING_MESSAGE_XXX)
    else:
        # subreddit could not be identified for some reason, eg trouble with the API, I'd recommend to have a
        return FLAIR_FLAIR_MISSING_MESSAGE_DEFAULT


# Unit Report ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
unitURL = "https://optc-db.github.io/common/data/units.js"
detailsURL = "https://optc-db.github.io/common/data/details.js"
cdURL = "https://optc-db.github.io/common/data/cooldowns.js"
unlocked_users = []

UNIT_STAT_NAME = ""
UNIT_STAT_TYPE = ""
UNIT_STAT_CLASS1 = ""
UNIT_STAT_CLASS2 = ""
UNIT_STAT_HP = ""
UNIT_STAT_ATK = ""
UNIT_STAT_RCV = ""
UNIT_STAT_SOCKETS = ""
UNIT_STAT_COMBO = ""
UNIT_STAT_CAPTAIN = ""
UNIT_STAT_SAILOR = ""
UNIT_STAT_SPECIAL = ""
UNIT_STAT_SPECIAL_NAME = ""
UNIT_STAT_SPECIAL_NOTES = ""
UNIT_STAT_COOLDOWN_MAX = ""
UNIT_STAT_COOLDOWN_MIN = ""

# Unit Report Messages ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MESSAGE_UNIT_REPORT_HEADER = "Ohayooooo~! I have attached the unit report for '" + UNIT_STAT_NAME + "' below!"
MESSAGE_UNIT_REPORT_NAME = "* ["
MESSAGE_UNIT_REPORT_TYPE = "](/"
MESSAGE_UNIT_REPORT_CLASS1 = ")\n\n  "
MESSAGE_UNIT_REPORT_CLASS2 = "/"
MESSAGE_UNIT_REPORT_HP = "\n\n  HP: "
MESSAGE_UNIT_REPORT_ATK = "  \n  ATK: "
MESSAGE_UNIT_REPORT_RCV = "  \n  RCV: "
MESSAGE_UNIT_REPORT_SOCKETS = "\n\n  Sockets:  "
MESSAGE_UNIT_REPORT_COMBO = "  \n  Combo: "
MESSAGE_UNIT_REPORT_CAPTAIN = "\n\n  **Abilities** \n  - **Captain**  \n  "
MESSAGE_UNIT_REPORT_SAILOR = "\n  - **Sailor**  \n  "
MESSAGE_UNIT_REPORT_SPECIAL1 = "  \n  - **Special** - "
MESSAGE_UNIT_REPORT_SPECIAL2 = "  "
MESSAGE_UNIT_REPORT_COOLDOWN1 = "  \n  *Cooldown "
MESSAGE_UNIT_REPORT_COOLDOWN2 = " → "
MESSAGE_UNIT_REPORT_COOLDOWN3 = "* \n"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
