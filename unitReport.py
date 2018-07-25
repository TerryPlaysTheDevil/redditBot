import json
import re
import urllib.request
import config as c
import logger as log


# Unit Reporter ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# File Updates ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def updateUnlockedUsers(subreddit):
    c.unlocked_users.clear()
    page = subreddit.wiki['mods/unlockedusers']
    namelist = page.content_md.split(';')
    for name in namelist:
        name = name.strip()
        name = name.lower()
        c.unlocked_users.append(name)
        if name == '':
            c.unlocked_users.remove(name)


def updateUnitFiles():
    urllib.request.urlretrieve(c.unitURL, filename=c.unitsPath)
    with open(c.unitsPath, "r") as unitsFile:
        text = unitsFile.read()
    text = text.replace("window.units = ", "")
    text = text.replace("    ", "")
    text = text.rsplit("],\n];")[0]
    text = text.replace("'6+'", '"6+"')
    text += "]\n]"
    try:
        with open(c.unitsPathTemp, "w") as file:
            file.write(text)
        with open(c.unitsPathTemp) as data:
            json.load(data)
        with open(c.unitsPath, "w") as file:
            file.write(text)
        log.updateSuccessful("updateUnitFiles")
    except Exception as e:
        log.updateFailed(e=e, location="updateUnitFiles")


def updateDetailsFiles():
    urllib.request.urlretrieve(c.detailsURL, filename=c.detailsPath)
    with open(c.detailsPath) as detailsFile:
        text = detailsFile.read()
    text = text.replace("window.details = ", "")
    i = 0
    indexes = re.finditer(r"    \d+", text)
    for index in indexes:
        end = text.__len__()
        text = (
            text[0:index.start() + 4 + 2 * i] + '"' + text[index.start() + 4 + 2 * i:index.end() + 2 * i] + '"' + text[
                                                                                                                  index.end() + 2 * i:end])
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
    # Cleaning the file end
    text = text.replace('},\n};', '}\n}')
    text = text.replace('},\n};', '}\n}')
    text = re.sub(r"(\},\n*[\s]*\n};)", "}\n}", text)
    # Remove comment artifacts
    text = re.sub(r"\/\/.*\n", "\n", text)
    try:
        with open(c.detailsPathTemp, "w") as file:
            file.write(text)
        with open(c.detailsPathTemp) as data:
            json.load(data)
        with open(c.detailsPath, "w") as file:
            file.write(text)
        log.updateSuccessful("updateDetailsFiles")
    except Exception as e:
        log.updateFailed(e=e, location="updateDetailsFile")


def updateCooldownsFiles():
    urllib.request.urlretrieve(c.cdURL, filename=c.cdPath)
    with open(c.cdPath, "r") as cdFile:
        text = cdFile.read()
    text = text.replace("window.cooldowns = ", "")
    text = text.rsplit(',', 1)[0] + "\n]"
    text = re.sub(r"\/\/.*\n", "\n", text)
    try:
        with open(c.cdPathTemp, "w") as file:
            file.write(text)
        with open(c.cdPathTemp) as data:
            json.load(data)
        with open(c.cdPath, "w") as file:
            file.write(text)
        log.updateSuccessful("updateCooldownsFiles")
    except Exception as e:
        log.updateFailed(e=e, location="updateCooldownsFile")


# Data Fetchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def unitReport(id):
    with open(c.unitsPath) as text:
        data = json.load(text)
    try:
        return data[int(id) - 1]
    except IndexError:
        return str("\n\n- The Index '" + id + "' is not linked to a unit in my database. Please make sure that you "
                                              "use a valid ID and try again.")


def detailReport(id):
    with open(c.detailsPath) as text:
        data = json.load(text)
    try:
        return data[str(id)]
    except KeyError:
        log.unhandledException(exception=KeyError, location="unitReport.detailReport()")


def cooldownReport(id):
    with open(c.cdPath) as text:
        data = json.load(text)
    return data[int(id) - 1]


# Report Building ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getName(unit):
    return unit[0]


def getTypes(unit):
    return str(unit[1]).lower()


def getClasses(unit):
    if isinstance(unit[2], str):
        return unit[2]
    else:
        return unit[2][0] + "/" + unit[2][1]


def getCombo(unit):
    return str(unit[5])


def getSockets(unit):
    return str(unit[6])


def getHP(unit):
    return str(unit[12])


def getATK(unit):
    return str(unit[13])


def getRCV(unit):
    return str(unit[14])


def buildStats(number):
    layout = 2  # TODO implement layouts
    unit = unitReport(number)
    if not isinstance(unit, str):
        c.UNIT_STAT_NAME = getName(unit)
        c.UNIT_STAT_TYPE = getTypes(unit)
        c.UNIT_STAT_CLASS = getClasses(unit)
        c.UNIT_STAT_COMBO = getCombo(unit)
        c.UNIT_STAT_SOCKETS = getSockets(unit)
        c.UNIT_STAT_HP = getHP(unit)
        c.UNIT_STAT_ATK = getATK(unit)
        c.UNIT_STAT_RCV = getRCV(unit)

        if layout == 1:
            text = c.MESSAGE_UNIT_REPORT_NAME + c.UNIT_STAT_NAME + c.MESSAGE_UNIT_REPORT_TYPE + c.UNIT_STAT_TYPE + \
                   c.MESSAGE_UNIT_REPORT_CLASS1 + c.UNIT_STAT_CLASS + c.MESSAGE_UNIT_REPORT_HP + c.UNIT_STAT_HP + \
                   c.MESSAGE_UNIT_REPORT_ATK + c.UNIT_STAT_ATK + c.MESSAGE_UNIT_REPORT_RCV + c.UNIT_STAT_RCV + \
                   c.MESSAGE_UNIT_REPORT_SOCKETS + c.UNIT_STAT_SOCKETS + c.MESSAGE_UNIT_REPORT_COMBO + c.UNIT_STAT_COMBO
        elif layout == 2:
            text = "\n* **[" + c.UNIT_STAT_NAME + "](http://optc-db.github.io/characters/#/view/" + number + ")** - " \
                                                                                                             "[" + \
                   c.UNIT_STAT_TYPE.upper() + "](/" + c.UNIT_STAT_TYPE + ") " + c.UNIT_STAT_CLASS + "  \n " + \
                   c.UNIT_STAT_HP + " HP | " + c.UNIT_STAT_ATK + " ATK | " + c.UNIT_STAT_RCV + " RCV  \n " + \
                   c.UNIT_STAT_SOCKETS + " Sockets, " + c.UNIT_STAT_COMBO + " CMB \n\n"
        return text


def getCaptain(details):
    try:
        return details["captain"]
    except KeyError:
        return "No captain ability"
    except TypeError:
        return "No captain ability"


def getSailor(details):
    try:
        return details["sailor"]
    except KeyError:
        return "No sailor ability"
    except TypeError:
        return "No sailor ability"


def getSpecial(details):
    i = 0
    multiLevelSpecial = 0
    text = ""
    try:
        if isinstance(details["special"], list):
            multiLevelSpecial = 1
            for stage in details["special"]:
                text += "  Stage " + str(i + 1) + ": " + stage["description"] \
                        + "  \n" + "*Cooldown "
                known = 0
                try:
                    text = text + str(stage["cooldown"][0]) + " → "
                    known = 1
                except Exception:
                    text += "not known*  \n"
                try:
                    if known == 1:
                        text = text + str(stage["cooldown"][1]) + "*  \n"
                except Exception:
                    text += "??*  \n"
                i += 1
        else:
            text = "  " + details["special"]
    except Exception:
        text = "  \n  No special ability"
    return text, multiLevelSpecial


def getCooldowns(cd):
    try:
        return str(cd[0]), str(cd[1])
    except Exception:
        return "??"


def preBuildAbilities(number):
    unit = unitReport(number)
    c.UNIT_STAT_NAME = getName(unit)
    c.UNIT_STAT_TYPE = getTypes(unit)
    c.UNIT_STAT_CLASS = getClasses(unit)
    return str(
        "  \n* **[" + c.UNIT_STAT_NAME + "](http://optc-db.github.io/characters/#/view/" + number + ")** - [" + c.UNIT_STAT_TYPE.upper() + "](/" + c.UNIT_STAT_TYPE + ") " + c.UNIT_STAT_CLASS
        + buildAbilities(number))


def buildAbilities(number):
    layout = 2
    details = detailReport(number)
    cd = cooldownReport(number)

    c.UNIT_STAT_CAPTAIN = getCaptain(details)
    c.UNIT_STAT_SAILOR = getSailor(details)

    temp = getSpecial(details)
    c.UNIT_STAT_SPECIAL = temp[0]
    multiLevelSpecial = temp[1]

    if not multiLevelSpecial:
        tempCD = getCooldowns(cd)
        if isinstance(tempCD, tuple):
            c.UNIT_STAT_COOLDOWN_MAX = tempCD[0]
            c.UNIT_STAT_COOLDOWN_MIN = tempCD[1]
        else:
            c.UNIT_STAT_COOLDOWN_MAX = tempCD
            c.UNIT_STAT_COOLDOWN_MIN = tempCD

    try:
        c.UNIT_STAT_SPECIAL_NAME = details["specialName"]
    except KeyError:
        c.UNIT_STAT_SPECIAL_NAME = "N/A"
    except TypeError:
        c.UNIT_STAT_SPECIAL_NAME = "N/A"
    except Exception:
        c.UNIT_STAT_SPECIAL_NAME = "N/A"
    if layout == 1:
        text = c.MESSAGE_UNIT_REPORT_CAPTAIN + c.UNIT_STAT_CAPTAIN + c.MESSAGE_UNIT_REPORT_SAILOR + \
               c.UNIT_STAT_SAILOR + c.MESSAGE_UNIT_REPORT_SPECIAL1 + c.UNIT_STAT_SPECIAL_NAME + \
               c.MESSAGE_UNIT_REPORT_SPECIAL2 + c.UNIT_STAT_SPECIAL + c.MESSAGE_UNIT_REPORT_SPECIAL2

        if not multiLevelSpecial:
            text += c.MESSAGE_UNIT_REPORT_COOLDOWN1 + c.UNIT_STAT_COOLDOWN_MAX + c.MESSAGE_UNIT_REPORT_COOLDOWN2 + \
                    c.UNIT_STAT_COOLDOWN_MIN + c.MESSAGE_UNIT_REPORT_COOLDOWN3
    if layout == 2:
        text = "\n * " + c.UNIT_STAT_CAPTAIN + "  \n * " + c.UNIT_STAT_SAILOR + "  \n * " + c.UNIT_STAT_SPECIAL
        if not multiLevelSpecial:
            text += "  \n  *Cooldown: " + c.UNIT_STAT_COOLDOWN_MAX + "* → *" + c.UNIT_STAT_COOLDOWN_MIN + "*"
    return text


def buildReport(number):
    statBlock = buildStats(number)
    abilityBlock = buildAbilities(number)
    return statBlock + abilityBlock


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



def updateFiles():
    try:
        updateUnitFiles()
        updateDetailsFiles()
        updateCooldownsFiles()
    except Exception as e:
        log.unhandledException(e, "unitResport.updateFiles()")
