from time import gmtime, strftime
import config as c


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


def unhandledException(exception, location):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " >>> Unhandled Exception '" + str(exception) + "' occured in '" + location +
               "'\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def successfulUpdate(location):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: UnitReport ::: '" + location + "' successfully updated all files\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def unitReported(comment):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: UnitReport ::: Created Unit Report for comment '" + comment + "'\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def newSubmission(submission):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: FlairBot ::: Submission '" + submission + "' has been created'\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def submissionRemoved(submission):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: FlairBot ::: Submission '" + submission + "' has been removed for not "
                                                                                       "adding a flair\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def submissionReinstated(submission):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: FlairBot ::: Submission '" + submission + "' has been reinstated after "
                                                                                       "adding a flair\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def submissionMonitoringStopped(submission):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: FlairBot ::: Submission '" + submission + "' has been removed from "
                                                                                "monitoring'\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def probationViolation(name, comment):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " ::: Probation ::: User " + name + " banned for Probation Violation ::: "
                                                                           "Trigger: " +
               comment + "\n")
    with open(c.logFile, "w") as log:
        log.write(newText)


def connectionError(name):
    with open(c.logFile, "r") as log:
        oldText = log.read()
    newText = (oldText + timestamp() + " >>> An error occurred when trying to connect to Reddit: " + name + "\n")
    with open(c.logFile, "w") as log:
        log.write(newText)
