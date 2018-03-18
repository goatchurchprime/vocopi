import time, datetime

tprevaction = 0
makestate = ""


coffeereport = [ "Coffee making report for "+datetime.datetime.now().isoformat(), "" ]

coffeesteps = [ "", "put the old filter into the compost", 
                "find a new coffee filter", 
                "add one measure of coffee to the filter", 
                "replace the filter funnel into machine", 
 #             "fill the jug with cold water", "pour water into the machine", "place jug on the hotplate", "turn on the machine", 
              "you are now done, wait for your coffee while I print the report" ]

def coffeemakingchecklist(words, say):
    global tprevaction, makestate
    print("cmc", words, makestate)
    if makestate == "commenced":
        say("Commencing the coffee making checklist.  Say check if done, or comment to add notes")
        makestate = 0
        words = ["check", "", "", ""]
        
    if words[0] == "repeat" or words[1] == "repeat":
        say("repeating item %d" % makestate)
        say(coffeesteps[makestate])
        return True
        
    if words[0] == "check":
        if makestate != 0:
            coffeereport.append("   "+datetime.datetime.now().isoformat()+"  check")
        makestate += 1
        say(coffeesteps[makestate])
        if makestate == len(coffeesteps) - 1:
            makestate = ""
            open("coffeereport.txt", "w").write("\n".join(coffeereport))
            return True
        coffeereport.append("")
        coffeereport.append(coffeesteps[makestate])
        return True
        
    if words[0] in ["close", "end", "stop"] and words[1] == "checklist":
        say("coffee making checklist aborted")
        makestate = ""
        return True
        
    if words[0] and type(makestate) == int:
        coffeereport.append("   "+datetime.datetime.now().isoformat()+" "+" ".join(words[:]))
        say("your comment on item %d has been noted" % makestate)
        return True
                
        
    say("You said "+" ".join(words)+" while making coffee")
    return True
    


def process(transcript, say):
    global tprevaction, makestate
    
    words = transcript.split()
    wc = len(words)
    tnow = time.time()
    dtime = tnow - tprevaction
    while len(words)<10:
        words.append("")
        
    if makestate:
        if makestate == "readytocommence":
            if dtime < 10 and words[0] == "coffee" and words[1] == "make":
                makestate = "commenced"
            else:
                makestate = ""
        coffeemakingchecklist(words, say)
        return True
        
    if words[0] == "coffee":
        if words[0] == "":
            say("say: coffee commands to get the command list")
            return True
        if words[1] == "commands":
            say("Available commands are: quantity, age, temperature, make")
            return True
        if words[1] == "quantity":
            say("There is half a pot left")
            return True
        if words[1] == "age":
            say("The coffee is 6 hours old")
            return True
        if words[1] == "temperature":
            say("The coffee is 36 degrees")
            return True
        if words[1] == "make":
            tprevaction = tnow
            if words[2] == "checklist":
                makestate = "commenced"
                coffeemakingchecklist(words, say)
                return True
            say("Say coffee make again to commence the coffee making checklist")
            makestate = "readytocommence"
            return True
                
            
    if wc == 1:
        say("one word")
    elif wc == 2:
        say("two words")
    elif wc == 3:
        say("three words")
    return False
	
