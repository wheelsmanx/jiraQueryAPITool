
from jira import JIRA
import requests
import json
import time

from datetime import datetime

jira = JIRA(options={'server' : '<jira URL>'} ,basic_auth=('user', 'pass'))

def requestRTC(ticket,url_Method):
    paramsForURL = {'ticket' : ticket}
    r = requests.get(url = url_Method, params = paramsForURL)

### method to add date and time to on screen std out logs 
def log_date(log_text):
    try:
        print(str("{:%B %d, %Y %H:%M:%S}".format(datetime.now())) + " " + log_text)
    except Exception as error: 
        print(str("{:%B %d, %Y %H:%M:%S}".format(datetime.now())) + " " + str(error))

### method to send ticket to not a bot sendBot('ticket number', 'ticket title')
def sendBot(y,x):
    if(True):
         requestRTC(y + " \n <jira URL>"+ y + " \n " + x, "<url to send the request to>")
    else: 
        log_date("Data Surpressed") 

### create cycle counter and temp dict to hold JQL infos
fromJiraJQLTickets = dict() 
counter = 0
while(True):
    fromJiraJQLTickets = dict() 
    for issue in jira.search_issues('"assignee is EMPTY ', maxResults=30):
        fromJiraJQLTickets[str(issue.key)] = str(issue.fields.summary)
        #requestRTC('{}: {}'.format(issue.key, issue.fields.summary), "<url to send the request to>")

    f = open("tickets.txt", "r+")
    try:
        ### try to load text file into json struct
        jiraTicketsFromFile = json.loads(f.read())
    except Exception as error:
        ### if it fails handle this error 
        log_date(error)
        jiraTicketsFromFile = "None"
        log_date("Exception: " + str(error))
    f.close()


    ### create copy of dict to write to text file at the end.
    tempTicketList = dict() 
    tempTicketList = fromJiraJQLTickets.copy()


    ### Compare JQL to text file json
    if(jiraTicketsFromFile == fromJiraJQLTickets):
        ### there are no new tickets in the queue
        log_date("Matches: No new RTC tickets it seems that the filter matches what is on file.")
    else:
        ### there are new tickets in the queue 
        log_date("New Ticket!: There is a new RTC ticket in the buffer ticket queue. Printing for Debug Info:")
        log_date("Older Filter: " + str(jiraTicketsFromFile))
        log_date("New Filter: " + str(fromJiraJQLTickets))
        log_date("Fileters do not match.")

        ### create copy of dict to write to text file at the end.
        
        ### check type of supposed dict to ensure that it is not a str as it will cause dict functions to fail 
        if(str(type(jiraTicketsFromFile)) == "<class 'str'>"):
            ### if it is a str handle it as this means the ticket.txt file is empty and all new tickets from JQL will be sent
            log_date("Error in dictionary structure on file. Skipping - Correction in next cycle.")
            for z, v in fromJiraJQLTickets.items():
                log_date("Sending to RTC bot: " + z)
                sendBot(z,v)

        else:
            ### type is not str and normal ticket comoparison can take place 
            for x, y in jiraTicketsFromFile.items():
                try:
                    del fromJiraJQLTickets[x]
                    ### remove tickets that are in both jiraTicketsFromFile and fromJiraJQLTickets
                except Exception as error: 
                    ### if this fails then log it - it should never fail. You would need to delete the text file while a comparison is taking place.
                    log_date("The item: " + x + " is not part of the tickets coming in. Comparison Error -- Likely that a ticket was taken and dropped from incomming.")
            ### normal Op mode -- send ticket to bot.
            for z, n in fromJiraJQLTickets.items():
                log_date("Sending to RTC bot: " + z)
                sendBot(z,n)


    ### write tempTicketList to the text file to ensure that we can compare it if it is restarted or w.e
               
    f= open("tickets.txt","r+")
    f.truncate()
    f.write(json.dumps(tempTicketList))
    f.close()
    log_date("Waiting....") 

    ### count the cycle and write it to stdout 
    
    counter = counter + 1
    log_date("Cycles ran for this instance: " + str(counter))

    ### wait 30 seconds
    time.sleep(30)



