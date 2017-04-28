import urllib.request, json, re
import config as c, logger as log


# Unit Reporter ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def updateUnitFiles():
    urllib.request.urlretrieve(c.unitURL, filename=c.unitsPath)
    with open(c.unitsPath, "r") as unitsFile:
        text = unitsFile.read()
    text = text.replace("window.units = ", "")
    text = text.replace("    ", "")
    text = text.rsplit("],\n];")[0]
    text += "]\n]"
    with open(c.unitsPath, "w") as unitsFile:
        unitsFile.write(text)


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
    text = text.replace('},\n};', '}\n}')
    # Remove comment artifacts
    text = re.sub(r"\/\/.*\n", "\n", text)
    with open(c.detailsPath, "w") as detailsFile:
        detailsFile.write(text)


def updateCooldownsFiles():
    urllib.request.urlretrieve(c.cdURL, filename=c.cdPath)
    with open(c.cdPath, "r") as cdFile:
        text = cdFile.read()
    text = text.replace("window.cooldowns = ", "")
    text = text.rsplit(',', 1)[0] + "\n]"
    text = re.sub(r"\/\/.*\n", "\n", text)
    with open(c.cdPath, "w") as cdFile:
        cdFile.write(text)


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
            UNIT_STAT_CAPTAIN = "No captain ability"
        except TypeError:
            UNIT_STAT_CAPTAIN = "No captain ability"
        
        try:
            UNIT_STAT_SAILOR = details["sailor"]
        except KeyError:
            UNIT_STAT_SAILOR = "No sailor ability"
        except TypeError:
            UNIT_STAT_SAILOR = "No sailor ability"
        
        UNIT_STAT_SPECIAL = ""
        i = 0
        try:
            if isinstance(details["special"], list):
                for stage in details["special"]:
                    UNIT_STAT_SPECIAL = UNIT_STAT_SPECIAL + "  \n  Stage " + str(i + 1) + ": " + stage["description"]
                    i += 1
        except TypeError:
            UNIT_STAT_SPECIAL = "  \n  No special ability"
        else:
            try:
                UNIT_STAT_SPECIAL = "  \n  " + details["special"]
            except KeyError:
                UNIT_STAT_SPECIAL = "  \n  No special ability"
            except TypeError:
                UNIT_STAT_SPECIAL = "  \n  No special ability"
        
        try:
            UNIT_STAT_SPECIAL_NAME = details["specialName"]
        except KeyError:
            UNIT_STAT_SPECIAL_NAME = "N/A"
        except TypeError:
            UNIT_STAT_SPECIAL_NAME = "N/A"
        
        try:
            UNIT_STAT_COOLDOWN_MAX = str(cd[0])
            UNIT_STAT_COOLDOWN_MIN = str(cd[1])
        except TypeError:
            UNIT_STAT_COOLDOWN_MAX = str("??")
            UNIT_STAT_COOLDOWN_MIN = str("??")
        
        return str(c.MESSAGE_UNIT_REPORT_NAME + UNIT_STAT_NAME + c.MESSAGE_UNIT_REPORT_TYPE + UNIT_STAT_TYPE + \
                   c.MESSAGE_UNIT_REPORT_CLASS1 + UNIT_STAT_CLASS + c.MESSAGE_UNIT_REPORT_HP + UNIT_STAT_HP + \
                   c.MESSAGE_UNIT_REPORT_ATK + UNIT_STAT_ATK + c.MESSAGE_UNIT_REPORT_RCV + UNIT_STAT_RCV + \
                   c.MESSAGE_UNIT_REPORT_SOCKETS + UNIT_STAT_SOCKETS + c.MESSAGE_UNIT_REPORT_COMBO + UNIT_STAT_COMBO
                   + \
                   c.MESSAGE_UNIT_REPORT_CAPTAIN + UNIT_STAT_CAPTAIN + c.MESSAGE_UNIT_REPORT_SAILOR + UNIT_STAT_SAILOR
                   + \
                   c.MESSAGE_UNIT_REPORT_SPECIAL1 + UNIT_STAT_SPECIAL_NAME + c.MESSAGE_UNIT_REPORT_SPECIAL2 +
                   UNIT_STAT_SPECIAL \
                   + c.MESSAGE_UNIT_REPORT_SPECIAL2 + c.MESSAGE_UNIT_REPORT_COOLDOWN1 + UNIT_STAT_COOLDOWN_MAX \
                   + c.MESSAGE_UNIT_REPORT_COOLDOWN2 + UNIT_STAT_COOLDOWN_MIN + c.MESSAGE_UNIT_REPORT_COOLDOWN3)
    else:
        return unit
        
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def updateFiles():
    try:
        updateUnitFiles()
        updateDetailsFiles()
        updateCooldownsFiles()
        log.successfulUpdate("unitReport.updateFiles()")
    except Exception as e:
        log.unhandledException(e, "unitResport.updateFiles()")
        
