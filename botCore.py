import platform
import re
import time

import config as c
import dbController as db
import flairEnforcer as flair
# import gacontrol as gac
import logger as log
import praw
import support as h
import unitReport as ur
import probation as prob


# Controllers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def liveMain():
    i = 0
    alreadyDoneForAutomod = []
    while 1:
        try:
            # checkFlairs is a fully functional Flair-Enforcer. It's currently disabled because no subreddit I moderate
            # requires me to host one of these.
            # checkFlairs(reddit=reddit, subreddit=subreddit)
            
            # Update all required files
            i = fileUpdate(i)
            
            for submission in subreddit.submissions(start=(int(time.time() - 90))):
                # Update Sidebar links to Megathreads
                alreadyDoneForAutomod = updateSidebar(moderator, submission, alreadyDoneForAutomod)
            
            for comment in subreddit.comments(limit=5):
                # Unit Reporter: !teach
                # initiateTeachingCheck(comment)
                # Unit Reporter: !unit !skills !stats
                # initiateUnitReportCheck(comment)
                # Probation Control
                if comment.author.name in c.giveaway_banned_users:
                    prob.probationControl(reddit=reddit, subreddit=subreddit, comment=comment)
                    # GA scans
                    # gac.initiateGAScans
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


def testMain():
    i = 0
    #    enforceTitle()
    while 1:
        try:
            time.sleep(60)
            # checkFlairs is a fully functional Flair-Enforcer. It's currently disabled because no subreddit I moderate
            # requires me to host one of these.
            # checkFlairs(reddit=reddit, subreddit=subreddit)
            
            # Update all required files
            i = fileUpdate(i)
            
            for submission in subreddit.new():
                # Update Sidebar links to Megathreads
                alreadyDoneForAutomod = updateSidebar(moderator, submission, alreadyDoneForAutomod)
            
            for comment in subreddit.comments(limit=5):
                if comment.author.name in c.giveaway_banned_users:
                    prob.probationControl(reddit=reddit, subreddit=subreddit, comment=comment)
                    # Unit Reporter: !teach
                    # initiateTeachingCheck(comment)
                    
                    # !Unit Reporter: !unit !skills !stats
                    # initiateUnitReportCheck(comment)
                    
                    # Probation Control
                    # GA scans
                    # gac.initiateGAScans
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


# def enforceTitle():
#    moderator.update(title=random.choice(c.approved_titles))


def initiateUnitReportCheck(comment):
    try:
        if comment.id not in c.ur_checked_comments and h.botHasNotAnswered(comment):
            i = 0
            output = ""
            if "!unit " in comment.body:
                regex = re.findall('!unit (\d+\s+)', comment.body)  # TODO CLEAN THIS UP
                regex_temp = re.findall('!unit (\w*\+?)', comment.body)
                regex_work = []
                for string in regex_temp:
                    if not h.is_number(string):
                        try:
                            unitID = db.isValid(string)
                        except Exception as e:
                            log.unhandledException(exception=e, location=initiateUnitReportCheck())
                        if unitID != False:
                            regex_work.append(unitID)
                        else:
                            output += "* The name '%s' could not be recognized. \n\n" % (string)
                            i += 1
                for number in regex:
                    number = number.strip(" ")
                    if h.is_number(number):
                        regex_work.append(number)
                for number in regex_work:
                    if i > 2:
                        break
                    number = str(number.lstrip('0'))
                    output += ur.buildReport(number)
                    i += 1
            
            if "!stats " in comment.body:
                regex = re.findall('!stats (\d+)', comment.body)
                for number in regex:
                    if i > 2:
                        break
                    number = str(number.lstrip('0'))
                    output += ur.buildStats(number)
                    i += 1
            
            if "!skills " in comment.body:
                regex = re.findall('!skills (\d+)', comment.body)
                for number in regex:
                    if i > 2:
                        break
                    number = str(number.lstrip('0'))
                    output += ur.preBuildAbilities(number)
                    i += 1
            
            if output != "":
                output += c.MESSAGE_FOOTER
                comment.reply(output)
                log.unitReported(comment.permalink(fast=True))
            c.ur_checked_comments.append(comment.id)
    except Exception as ex:
        log.unhandledException(exception=ex, location="botCore.initiateUnitReportCheck()")


def initiateTeachingCheck(comment):
    try:
        if comment.id not in c.t_checked_comments and h.botHasNotAnswered(comment):
            i = 0
            output = ""
            if "!teach " in comment.body:
                output = "The following units have been added: \n\n"
                regex = re.findall('!teach (\w+\W?:\d+)', comment.body)
                for string in regex:
                    if i >= 25:
                        output += "However, the maximum for units to be added in a single post has been exceeded, " \
                                  "so some of your input could not be added anymore. Please try again in a new comment."
                        break
                    string = string.split(":")
                    output += " * %s \n" % (db.addNameID(name=string[0].lower(), id=string[1]))
                    i += 1
            
            if output != "":
                comment.reply(output + c.MESSAGE_FOOTER)
            c.t_checked_comments.append(comment.id)
    
    
    except Exception as e:
        print(e)
        log.unhandledException(exception=e, location="initiateTeachingCheck()")


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


def fileUpdate(i):
    if i == 0 or i == 1000:
        # ur.updateUnlockedUsers(subreddit)
        prob.updateBannedUsers(subreddit)
        # ur.updateFiles()
        updateModerators()
        i = 1
    return i + 1


def updateModerators():
    c.SUB_MODERATORS.clear()
    for mod in subreddit.moderator():
        c.SUB_MODERATORS.append(mod.name)


def updateSidebar(moderator, submission, alreadyDoneForAutoMod):
    submission = subreddit.su
    if submission.id not in alreadyDoneForAutoMod:
        if " Weekly Questions & Advice Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[BOTH\]\(.*\)\|Questions & Advice Megathread\|",
                                 "[BOTH](" + submission.shortlink + ")|Questions & Advice Megathread|", sidebarText)
            log.sidebar("Q&A")
            moderator.update(description=sidebarText)
        
        elif " Weekly Friend Request Megathread" in submission.title and "[ENG]" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[ENG\]\(.*\)\|Friend Request Megathread\|",
                                 "[ENG](" + submission.shortlink + ")|Friend Request Megathread|", sidebarText)
            log.sidebar("FR ENG")
            moderator.update(description=sidebarText)
        
        elif " Weekly Friend Request Megathread" in submission.title and "[JPN]" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\|Friend Request Megathread\|\[JPN\]\(.*\)",
                                 "|Friend Request Megathread|[JPN](" + submission.shortlink + ")", sidebarText)
            log.sidebar("FR JPN")
            moderator.update(description=sidebarText)
        
        elif "[ENG] Weekly Updated Giveaway Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[ENG\]\(.*\)\|Account Giveaway Megathread\|",
                                 "[ENG](" + submission.shortlink + ")|Account Giveaway Megathread|", sidebarText)
            log.sidebar("GA ENG")
            moderator.update(description=sidebarText)
        
        elif "[JPN] Weekly Updated Giveaway Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\|Account Giveaway Megathread\|\[JPN\]\(.*\)",
                                 "|Account Giveaway Megathread|[JPN](" + submission.shortlink + ")", sidebarText)
            log.sidebar("GA JPN")
            moderator.update(description=sidebarText)
        
        elif "Weekly Character Concepts Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[Weekly Character Concepts\](.*)",
                                 "[Weekly Character Concepts](/" + submission.id + " 'Megathread')", sidebarText)
            log.sidebar("Char Concepts")
            moderator.update(description=sidebarText)
        
        elif "Weekly Rant Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[Weekly Rants\](.*)",
                                 "[Weekly Rants](/" + submission.id + " 'Megathread')", sidebarText)
            log.sidebar("Rants")
            moderator.update(description=sidebarText)
        
        elif "Weekly Achievements Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[Weekly Achievements\](.*)",
                                 "[Weekly Achievements](/" + submission.id + " 'Megathread')", sidebarText)
            log.sidebar("Achievements")
            moderator.update(description=sidebarText)
        
        elif "Mentoring Megathread" in submission.title and submission.author.name in c.SUB_MODERATORS:
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub("\[Mentoring Megathread\](.*)",
                                 "[Mentoring Megathread](/" + submission.id + " 'Megathread')", sidebarText)
            log.sidebar("Achievements")
            moderator.update(description=sidebarText)
        
        elif "missing videos" in submission.title.lower() and (submission.author.name == "snookajab" or submission.author.name == "TheEmperor1k"):
            settings = moderator.settings()
            sidebarText = settings['description']
            sidebarText = re.sub('Global Clear Rates\]\((\S)* "Missing Videos"\)',
                                 'Global Clear Rates](' + submission.shortlink + ' "Missing Videos")', sidebarText)
            log.sidebar("Missing Videos")
            moderator.update(description=sidebarText)
        
        alreadyDoneForAutoMod.append(submission.id)
    return alreadyDoneForAutoMod


# Initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    reddit = praw.Reddit(client_id=c.BOT_LOGIN_CLIENT_ID, client_secret=c.BOT_LOGIN_SECRET, username=c.BOT_LOGIN_NAME,
                         password=c.BOT_LOGIN_PASSWORD, user_agent=c.BOT_USER_AGENT)
    subreddit = reddit.subreddit(c.BOT_SUBREDDIT_TO_MONITOR)
    moderator = subreddit.mod
    if platform.system() == "Windows":
        testMain()
    else:
        liveMain()
