import sqlite3


def getID(name):
    name = name.lower()
    namesDB = sqlite3.connect("files/names.db")
    c = namesDB.cursor()
    c.execute("""SELECT "id" FROM units WHERE (name = "%s")""" % name)
    data = c.fetchone()[0]
    namesDB.close()
    return str(data)


def addNameID(name, id):
    namesDB = sqlite3.connect("files/names.db")
    c = namesDB.cursor()
    try:
        c.execute("""INSERT INTO units (name, id) VALUES ("%s", "%s");""" % (name, id))
        output = "Name: %s - ID: %s" % (name, id)
    except sqlite3.IntegrityError:
        output = "The name '%s' was already stored in the database before processing your request." % name
    finally:
        namesDB.commit()
        namesDB.close()
        return output


def isValid(string):
    try:
        return getID(string)
    except:
        return False
