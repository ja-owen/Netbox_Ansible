def logging(logstring):
    f = open("actionlog.log","a+")
    f.write(logstring)
    f.close()

def dblogging(logstring):
    f = open("dblog.log","a+")
    f.write(logstring)
    f.close()