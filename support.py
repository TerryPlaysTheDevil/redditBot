def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def botHasNotAnswered(comment):
    for reply in comment.replies:
        if reply.author.name == "OPTCBot":
            return False
    return True