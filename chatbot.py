import Legobot
import ConfigParser

TIP_DICT = {}

def helloWorld(msg):
    return "Hello, world!"

def is_num(val):
    try:
        if float(val) != int(val):
            return False

        test = int(val)
        test = int(float(val))

        return True
    except:
        return False

def tip_user(msg):
    """
    Inputs:
      takes msg which is a cMsg object

    Outputs:
      returns string to echo back to user in IRC

    Purpose:
      allows users to tip other users (must be in our engineer list) magical imaginary points
      Usage:
      !tip [nick] [points]
    """
    if msg.arg1 is None or msg.arg2 is None:
        #must have 2 args
        returnVal = fGetHelpText(msg.cmd)
        
    elif msg.arg1 in msg.userInfo:
        returnVal = "You can't tip yourself!"
    
    elif not is_num(msg.arg2):
        returnVal = "Incorrect Syntax, you must tip a number"
        
    else:
        #proper number of args
        if msg.arg1 in TIP_DICT:
            TIP_DICT[msg.arg1] += int(msg.arg2)
        else:
            TIP_DICT[msg.arg1] = int(msg.arg2)

        returnVal = "%s tipped, and now has %s internet points" % (msg.arg1, TIP_DICT[msg.arg1])
    return returnVal

def print_tips(msg):
    """
    Inputs:
        takes junk which is a cMsg object: optional and unused

    Outputs:
        returns string to echo back to user in IRC

    Purpose:
        allows users to view current tips.    Usage:
        !printtips
    """
    
    
    tips = ["%s: %s" % (k, v) for k, v in TIP_DICT.items()]
    if len(tips) == 0:
        returnVal = "No tips yet!"
    else:
        returnVal = "Current Tips: %s" % (", ".join(tips))
    return returnVal

def cointoss(msg):
    import random
    """
    Inputs:
      takes msg object

    Outputs:
      returns string to echo back to user in IRC

    Purpose:
      flip an imaginary coin or roll an imaginary x sided die
      Usage:
      !roll [# of sides]
    """

    if not msg.arg1:
        toss = random.randint(0,1)
        if toss == 0:
            returnVal = "Heads"
        else:
            returnVal = "Tails"
    else:
        if not is_num(msg.arg1):
            returnVal = "Incorrect syntax. You must use a (sane) number"
        elif is_num(msg.arg1) and not int(msg.arg1) >= 2:
            returnVal = "No. Use two or more sides."
        elif is_num(msg.arg1) and int(msg.arg1) == 2:
            toss = random.randint(1,2)
            if toss == 1:
                returnVal = "Heads"
            else:
                returnVal = "Tails"
        else:
            toss = random.randint(1,int(msg.arg1))
            returnVal = str(toss)
    return returnVal

def xkcd(msg):
    import urllib2, re
    webpage = urllib2.urlopen('http://dynamic.xkcd.com/random/comic')
    webpage = webpage.read()
    print webpage
    comic = re.search(r'<div id="comic".*?\n?.*?(//im.+?)".+?\s?title="(.+?)"',webpage)
    if comic:
        altText = comic.group(2).replace("&#39;","'")
        returnVal = "%s %s" %(altText,"http:" + comic.group(1))
        return returnVal

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('chatbot.cfg')
    HOST = config.get('Main','host')
    PORT = config.getint('Main','port')
    NICK = config.get('Main','nick')

    try:
        HOSTPW = config.get('Main','hostpw')
    except:
        print "Host password not found, skipping..."

    CHANS = []
    for (key, val) in config.items('Channels'):
        chan = None
        chan_pass = None
        val = val.strip()
        val = val.split(' ')
        
        if len(val) == 1:
            chan = val[0]
        if len(val) == 2:
            chan = val[0]
            chan_pass = val[1]

        if chan_pass:
            CHANS.append((chan,chan_pass))
        else:
            CHANS.append((chan,''))


    mybot = Legobot.legoBot(host=HOST,port=PORT,nick=NICK,chans=CHANS,hostpw=HOSTPW)
    mybot.addFunc("!helloworld", helloWorld, "Ask your bot to say hello. Usage: !helloworld")
    mybot.addFunc("!roll", cointoss, "Roll a magical N-sided die. Usage !roll [ N>1 sides ]")
    mybot.addFunc("!xkcd", xkcd, "Pulls a random XKCD comic. Usage: !xkcd")
    mybot.addFunc("!tip", tip_user, "Tip a specific user. Usage !tip [user]")
    mybot.connect(isSSL=True)




if __name__ == "__main__":
    main()
