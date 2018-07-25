import praw, config as c, logger as log


# Probation Bot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def updateBannedUsers(subreddit):
    c.giveaway_banned_users.clear()
    page = subreddit.wiki['mods/giveawaybans']
    namelist = page.content_md.split(';')
    for name in namelist:
        c.giveaway_banned_users.append(name.strip())
        if name == '':
            c.giveaway_banned_users.remove(name)


def probationControl(reddit, subreddit, comment):
    if " Weekly Updated Giveaway Megathread" in comment.submission.title and comment.permalink not in \
            c.giveaway_handled:
        try:
            comment.mod.remove()
            reddit.redditor(comment.author.name).message(subject=c.giveaway_ban_message_title,
                                                         message=(c.giveaway_ban_message_1 +
                                                                  comment.author.name + c.giveaway_ban_message_2))
            c.giveaway_handled.append(comment.permalink)
            log.probationViolation(name=comment.author.name, comment=comment.permalink)
            subreddit.message(subject="Probation Violation - " + comment.author.name, message="u/" +
                    comment.author.name + " has broken his probation. Please investigate as soon as possible.")
            #subreddit.banned.add(comment.author.name, ban_reason='OPTCBot: Account Hoarding - Automatic Ban for '
            #                                                     'Probation Violation')
        except Exception as e:
            log.unhandledException(exception=e, location="probation.probationControl()")
