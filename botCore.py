import praw, urllib.request, json, time, requests, pprint, re

# Configuration Section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BOT_SUBREDDIT_TO_MONITOR = "OnePieceTC"
BOT_LOGIN_NAME = "OPTCBot"
BOT_LOGIN_PASSWORD = "wrSQHSSMsrKHm$@Xu7g8&$nN6P9hCtYJD*H2sRh@bMF"
BOT_USER_AGENT = "Subreddit monitoring and moderation bot with some subreddit specific functionalities for /r/OnePieceTC by /u/lolTerryP"
# Message Footer
MESSAGE_FOOTER = "\n\n-----\n**[Please read this.](/str)** I am a bot in development by /u/lolTerryP. If you have a suggestion or a question, feel free to PM" \
                 " him by clicking [here](https://www.reddit.com/message/compose?to=lolTerryP&subject=OPTCBot).  \nA really big thanks to the great guys at OPTC-DB " \
                 "who provided me with the data I need for this feature!"

# OPTC-DB API URLs
unitURL = "https://optc-db.github.io/common/data/units.js"
unitsPath = "C:/redditBot/units.txt"
detailsURL = "https://optc-db.github.io/common/data/details.js"
detailsPath = "C:/redditBot/details.txt"
cdURL = "https://optc-db.github.io/common/data/cooldowns.js"
cdPath = "C:/redditBot/cooldowns.txt"

# Unit Report Stats
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
UNIT_STAT_CAPTAIN_NAME = ""
UNIT_STAT_SAILOR = ""
UNIT_STAT_SPECIAL = ""
UNIT_STAT_SPECIAL_NAME = ""
UNIT_STAT_SPECIAL_NOTES = ""
UNIT_STAT_COOLDOWN_MAX = ""
UNIT_STAT_COOLDOWN_MIN = ""

# Unit Report Messages
MESSAGE_UNIT_REPORT_HEADER = "Ohayooooo~! I have attached the unit report for '" + UNIT_STAT_NAME + "' below, Terry-sama! Hai, hai, desu! *giggles*\n\n"
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


# Unit Reporter ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def updateUnitFiles():
    urllib.request.urlretrieve(unitURL, filename=unitsPath)
    with open(unitsPath, "r") as unitsFile:
        text = unitsFile.read()
    text = text.replace("window.units = ", "")
    text = text.replace("    ", "")
    text = text.rsplit("],\n];")[0]
    text = text + ("]\n]")
    with open(unitsPath, "w") as unitsFile:
        unitsFile.write(text)


def updateDetailsFiles():
    urllib.request.urlretrieve(detailsURL, filename=detailsPath)
    with open(detailsPath) as detailsFile:
        text = detailsFile.read()
    text = text.replace("window.details = ", "")
    i = 0
    indexes = re.finditer(r"    \d+", text)
    for index in indexes:
        end = text.__len__()
        text = (
            text[0:index.start() + 4 + 2 * i] + '"' + text[index.start() + 4
                        + 2 * i:index.end() + 2 * i] + '"' + text[index.end() + 2 * i:end])
        i += 1
    # Fix the JSON
    text = text.replace('special:', '"special":')
    text = text.replace('specialName', '"specialName"')
    text = text.replace('captain:', '"captain":')
    text = text.replace('specialNotes', '"specialNotes"')
    text = text.replace('captainNotes', '"captainNotes"')
    text = text.replace('sailor:', '"sailor":')
    text = text.replace('sailorNotes', '"sailorNotes"')
    text = text.replace(' )}",\n    },', ' )}"\n    },')
    text = text.replace('},\n        ],', '}\n        ],')
    text = text.replace('",\n    },', '"\n    },')
    text = text.replace('],\n            }', ']\n            }')
    text = text.replace('], \n            }', '] \n            }')
    text = text.replace('},\n};', '}\n}')
    # Remove comment artifacts
    text = re.sub(r"\/\/.*\n", "\n", text)
    with open(detailsPath, "w") as detailsFile:
        detailsFile.write(text)


def updateCooldownsFiles():
    urllib.request.urlretrieve(cdURL, filename=cdPath)
    with open(cdPath, "r") as cdFile:
        text = cdFile.read()
    text = text.replace("window.cooldowns = ", "")
    text = text.rsplit(',', 1)[0] + "\n]"
    text = re.sub(r"\/\/.*\n", "\n", text)
    with open(cdPath, "w") as cdFile:
        cdFile.write(text)


def unitReport(id):
    with open(unitsPath) as text:
        data = json.load(text)
    try:
        return data[int(id) - 1]
    except IndexError:
        return str("\n\n- The Index '" + id + "' is not linked to a unit in my database. Please make sure that you use a valid ID and try again.")


def detailReport(id):
    with open(detailsPath) as text:
        data = json.load(text)
    return data[str(id)]


def cooldownReport(id):
    with open(cdPath) as text:
        data = json.load(text)
    return data[int(id) - 1]


def buildReport(number):
    unit = unitReport(number)
    if not isinstance(unit, str):
        details = detailReport(number)
        cd = cooldownReport(number)

        UNIT_STAT_NAME = unit[0]
        UNIT_STAT_TYPE = str(unit[1]).lower()
        if isinstance(unit[2], str):
            UNIT_STAT_CLASS = unit[2]
        else:
            UNIT_STAT_CLASS = unit[2][0] + "/" + unit[2][1]
        UNIT_STAT_COMBO = str(unit[5])
        UNIT_STAT_SOCKETS = str(unit[6])
        UNIT_STAT_HP = str(unit[12])
        UNIT_STAT_ATK = str(unit[13])
        UNIT_STAT_RCV = str(unit[14])

        try:
            UNIT_STAT_CAPTAIN = details["captain"]
        except KeyError:
            UNIT_STAT_CAPTAIN = "None"

        try:
            UNIT_STAT_SAILOR = details["sailor"]
        except KeyError:
            UNIT_STAT_SAILOR = "None"

        UNIT_STAT_SPECIAL = ""
        i = 0
        if isinstance(details["special"], list):
            for stage in details["special"]:
                UNIT_STAT_SPECIAL = UNIT_STAT_SPECIAL + "  \n  Stage " + str(i + 1) + ": " + stage["description"]
                i += 1
        else:
            try:
                UNIT_STAT_SPECIAL = "  \n  " + details["special"]
            except KeyError:
                UNIT_STAT_SPECIAL = "  \n  None"
        try:
            UNIT_STAT_SPECIAL_NAME = details["specialName"]
        except KeyError:
            UNIT_STAT_SPECIAL_NAME = ""


        try:
            UNIT_STAT_COOLDOWN_MAX = str(cd[0])
            UNIT_STAT_COOLDOWN_MIN = str(cd[1])
        except TypeError:
            UNIT_STAT_COOLDOWN_MAX = str("??")
            UNIT_STAT_COOLDOWN_MIN = str("??")

        return str(MESSAGE_UNIT_REPORT_NAME + UNIT_STAT_NAME + MESSAGE_UNIT_REPORT_TYPE + UNIT_STAT_TYPE + \
                 MESSAGE_UNIT_REPORT_CLASS1 + UNIT_STAT_CLASS + MESSAGE_UNIT_REPORT_HP + UNIT_STAT_HP + \
                 MESSAGE_UNIT_REPORT_ATK + UNIT_STAT_ATK + MESSAGE_UNIT_REPORT_RCV + UNIT_STAT_RCV + \
                 MESSAGE_UNIT_REPORT_SOCKETS + UNIT_STAT_SOCKETS + MESSAGE_UNIT_REPORT_COMBO + UNIT_STAT_COMBO + \
                 MESSAGE_UNIT_REPORT_CAPTAIN + UNIT_STAT_CAPTAIN + MESSAGE_UNIT_REPORT_SAILOR + UNIT_STAT_SAILOR + \
                 MESSAGE_UNIT_REPORT_SPECIAL1 + UNIT_STAT_SPECIAL_NAME + MESSAGE_UNIT_REPORT_SPECIAL2 + UNIT_STAT_SPECIAL \
                 + MESSAGE_UNIT_REPORT_SPECIAL2 + MESSAGE_UNIT_REPORT_COOLDOWN1 + UNIT_STAT_COOLDOWN_MAX \
                 + MESSAGE_UNIT_REPORT_COOLDOWN2 + UNIT_STAT_COOLDOWN_MIN + MESSAGE_UNIT_REPORT_COOLDOWN3)
    else:
        return unit
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Probation Bot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
reddit = praw.Reddit(client_id="xEKIjwnolMirSw", client_secret="ZIwaJdNWO8aZRy0bWnDzFch5jcA", username=BOT_LOGIN_NAME,
                     password=BOT_LOGIN_PASSWORD, user_agent=BOT_USER_AGENT)
subreddit_1 = reddit.subreddit("OnePieceTC")

updateUnitFiles()
updateDetailsFiles()
updateCooldownsFiles()
# buildReport(1338)

for comment in subreddit_1.stream.comments():
    if
    if "!unit " in comment.body and comment.author == "lolTerryP":
        regex = re.findall('!unit (\d+)', comment.body)
        output = ""
        i = 0
        for number in regex:
            if i >= 5:
                break
            output += buildReport(number)
            i += 1
        output += MESSAGE_FOOTER
        comment.reply(output)
        print("Replied to " + comment.permalink(fast=True))
        output = ""
