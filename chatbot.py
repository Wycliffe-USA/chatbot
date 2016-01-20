import Legobot
import ConfigParser

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
    #Initialize empty list of tipped users
    import os

    tipped = []
    nick_to_tip = msg.arg1
    amt_to_tip = msg.arg2

    tips_file = ConfigParser.SafeConfigParser()
    if os.path.isfile('tips.cfg'):
        tips_file.read('tips.cfg')
    else:
        return "No tips found. Please initialize a tips.cfg file."

    try:
        for (key,value) in tips_file.items('Tips'):
            tipped.append(key)
    except Exception as e:
        return e

    if nick_to_tip is None or amt_to_tip is None:
        #must have 2 args
        return "wat?"
        
    else:
        #proper number of args
        if nick_to_tip in tipped:
            #user already exists. get value, increment, write back to configparse obj
            tipval = tips_file.get('Tips',nick_to_tip)
            tipval = int(amt_to_tip) + int(tipval)
            tips_file.set('Tips',nick_to_tip,str(tipval))
        else:
            tipval = amt_to_tip
            tips_file.set('Tips',nick_to_tip,str(tipval))

        tipval = tips_file.get('Tips',nick_to_tip)
        returnVal = "%s tipped %s internet points, giving them a total of %s" % (nick_to_tip, str(amt_to_tip), tipval)
    with open('tips.cfg','wb') as f:
        tips_file.write(f)
    return returnVal

def print_tips(msg):
    import os
    import ConfigParser

    tips_file = ConfigParser.SafeConfigParser()
    if os.path.isfile('tips.cfg'):
        tips_file.read('tips.cfg')
    else:
        return "No tips found. Please initialize a tips.cfg file."
    
    if msg.arg1:
        try:
            tipval = tips_file.get('Tips',msg.arg1)
            returnval = "%s has %s meaningless internet points." % (msg.arg1, tipval)
        except:
            returnval = "I don't think %s has been tipped yet. Poor, pointless soul." % msg.arg1
    else:    
        try:
            tipped = []
            for (key,value) in tips_file.items('Tips'):
                tipped.append("%s: %s" % (key, value))
        except Exception as e:
            return e
        tipped = ", ".join(tipped)
        returnval = "Current tips: %s" % tipped
    return returnval

def check_weather_by_zip(msg):
    # check_weather_by_zip
    # Uses the Weather Underground API to check current conditions and a forecast
    # Pulls its API key from api.cfg file in the same directory as your bot. 

    import ConfigParser
    import re
    import requests
    import os

    if not msg.arg1:
        return "Please provide a zip code for me to check"
    else:
        if re.match(r'^\d{5}$',msg.arg1) is not None:
            pass
        else:
            return "I only support 5 digit, US zip codes."

    api_keys = ConfigParser.SafeConfigParser()
    if os.path.isfile('api.cfg'):
        api_keys.read('api.cfg')
    else:
        return "No API keys found. Please initialize your api.cfg file."

    try:
        WUNDERGROUND_API_KEY = api_keys.get('API','wunderground')
    except Exception as e:
        return e


    zipcode = msg.arg1
    current = requests.get("http://api.wunderground.com/api/%s/conditions/q/%s.json" % (WUNDERGROUND_API_KEY, zipcode))
    forecast = requests.get("http://api.wunderground.com/api/%s/forecast/q/%s.json" % (WUNDERGROUND_API_KEY, zipcode))
    current = current.json()
    forecast = forecast.json()
    try: 
        location = current['current_observation']['display_location']['full']
        condition = current['current_observation']['weather']
        temp_f = current['current_observation']['temp_f']
        humidity = current['current_observation']['relative_humidity']
        feelslike_f = current['current_observation']['feelslike_f']
        wind_condition = current['current_observation']['wind_string']
        wind_dir = current['current_observation']['wind_dir']
        wind_speed = current['current_observation']['wind_mph']
        wind_gust = current['current_observation']['wind_gust_mph']

        short_forecast_period = forecast['forecast']['txt_forecast']['forecastday'][1]['title']
        short_forecast_data = forecast['forecast']['txt_forecast']['forecastday'][1]['fcttext']

        forecast_url = current['current_observation']['forecast_url']

    except: 
        return "Unable to find information on that zip code right now. Please check again later or petition Congress to have it created."

    reply = "The weather in %s is currently %s with a temperature of %s degrees, humidity of %s, and it feels like %s degress. Wind is %s, blowing %s at %s mph with %s mph gusts. Forecast for %s: %s" % (
        location,
        condition,
        temp_f,
        humidity,
        feelslike_f,
        wind_condition,
        wind_dir,
        wind_speed,
        wind_gust,
        short_forecast_period,
        short_forecast_data,
        )
    return reply

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

    config.read("chatbot.cfg")
    HOST = config.get('Main','host')
    PORT = config.getint('Main','port')
    NICK = config.get('Main','nick')
    HOSTPW = None

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

    if HOSTPW:
        mybot = Legobot.legoBot(host=HOST,port=PORT,nick=NICK,chans=CHANS,hostpw=HOSTPW)
    else:
        mybot = Legobot.legoBot(host=HOST,port=PORT,nick=NICK,chans=CHANS)
    #mybot.addFunc("!helloworld", helloWorld, "Ask your bot to say hello. Usage: !helloworld")
    mybot.addFunc("!roll", cointoss, "Roll a magical N-sided die. Usage !roll [ N>1 sides ]")
    #mybot.addFunc("!xkcd", xkcd, "Pulls a random XKCD comic. Usage: !xkcd")
    mybot.addFunc("!tip", tip_user, "Tip a specific user. Usage !tip [user]")
    mybot.addFunc("!weather", check_weather_by_zip, "Check weather by zipcode. Usage: !weather 36429")
    mybot.addFunc('!printtips', print_tips, "See who has been tipped")
    mybot.connect(isSSL=True)




if __name__ == "__main__":
    main()
