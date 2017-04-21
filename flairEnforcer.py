import time
import config as c


#  Flair Enforcer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def removeUnflairedSubmission(self, id, reddit, id_for_replies):
    reddit.submission(id=id).mod.remove()
    replyText = c.decideSubreddit(reddit.submission(id).subreddit)
    reply = reddit.submission(id=id).reply(body=(replyText + c.MESSAGE_FOOTER))
    reply.mod.distinguish()
    id_for_replies[id] = reply.id


def reinstateSubmission(self, id, reddit, id_for_replies):
    reddit.submission(id=id).mod.approve()
    reddit.comment(id=id_for_replies[id]).mod.remove()
    del id_for_replies[id]


def checkNewSubmissions(self, subreddit, approved_submissions, submissions_with_no_flair):
    # Get 25 new submissions from the sub
    for submission in subreddit.new(limit=c.SUBMISSION_FETCH_LIMIT):
        # If the submission is unprocessed, add it to the procedure
        if submission.link_flair_text is None and submission.id not in submissions_with_no_flair and \
                        submission.id not \
                        in approved_submissions and (time.time() - submission.created_utc) > c.FLAIR_FIRST_GRACE_PERIOD:
            submissions_with_no_flair.append(submission.id)


def revisitSubmissions(self, reddit, approved_submissions, submissions_with_no_flair, removed_submissions,
                       id_for_replies):
    for id in submissions_with_no_flair:
        # Submission is not flaired and younger than 5 minutes
        if reddit.submission(id=id).link_flair_text is None and (time.time() - reddit.submission(
                id=id).created_utc) \
                < c.FLAIR_TIME_LIMIT and id not in removed_submissions:
            print(str(time.time() - reddit.submission(id=id).created_utc) + " ::: " + id + " unflaired, removing")
            removeUnflairedSubmission(id=id, reddit=reddit, id_for_replies=id_for_replies)
            removed_submissions.append(id)
        
        # Submission is not flaired and younger than 5 minutes, but has been removed already
        elif reddit.submission(id=id).link_flair_text is None and (
                    time.time() - reddit.submission(id=id).created_utc) \
                < c.FLAIR_TIME_LIMIT and id in removed_submissions:
            print(str(time.time() - reddit.submission(id=id).created_utc) + " ::: " + id + " still unflaired")
        
        # Submission has been flaired
        elif reddit.submission(id=id).link_flair_text is not None:
            submissions_with_no_flair.remove(id)
            print(str(
                time.time() - reddit.submission(id=id).created_utc) + " ::: " + id + " flair added, reinstating")
            reinstateSubmission(id=id, reddit=reddit, id_for_replies=id_for_replies)
            approved_submissions.append(id)
        
        # Submission has not been flaired and is now older than 5 minutes
        elif time.time() - reddit.submission(id=id).created_utc >= c.FLAIR_TIME_LIMIT:
            submissions_with_no_flair.remove(id)
            print(str(time.time() - reddit.submission(id=id).created_utc) + " ::: " + id + " time out")
            approved_submissions.append(id)
        # Something else happened, should actually never be triggered
        else:
            print(
                "Timestamp: " + str(time.time()) + " - " + str(
                    reddit.submission(id=id).created_utc) + " - Flairtext: "
                                                            "" + str(
                    reddit.submission(id)) + " ::: SOMETHING HAPPENED")
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
