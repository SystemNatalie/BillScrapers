import json
import urllib3
import sqlite3
http = urllib3.PoolManager()
#gotten via inspection of requests made by this website https://alison.legislature.state.al.us/bill-search
#uses graphql
graphql_url = "https://alison.legislature.state.al.us/graphql/"
get_current_session_query = json.dumps(
    {
        "operationName":"config",
        "query":"""query config {
                    currentSession: session(where: {current: {eq: true}}) {
                        name
                        abbreviation
                        legislativeDay
                        startDate
                        endDate
                        __typename
                    }
                    prefileSession: session(where: {prefile: {eq: true}}) {
                        name
                        abbreviation
                        __typename
                    }
                   }""",
        "variables":{}
    }
)#todo idk if we need the prefileSession
response = http.request("POST", graphql_url, body=get_current_session_query,headers={'Content-Type': 'application/json'})
response_data = json.loads(response.data.decode('utf-8'))

#TODO paginate?
#TODO check if updated in DB in order to determine if we get the full text
#TODO [switched to pdfs. not an issue? line 36 is relevant] downloading plaintext may not be the best thing to do... we could download PDF's but that adds a lot of load (both network and processing wise.)
session = response_data['data']['currentSession']['name']
#get_bill_text_and_deets_query = json.dumps({"query":"query{instrumentOverviews(where: {sessionType: {eq:\""+session+"\"}}){count,data{instrumentType,instrumentVersionNbr,subject,instrumentNbr,shortTitle,createdAt,updatedAt, introducedDate, confirmedDate, actSummary,lastAction, body, fullText,introducedUrl,enrolledUrl}}}","variables":{}})
get_bill_text_and_deets_query = json.dumps({"query":"query{instrumentOverviews(where: {sessionType: {eq:\""+session+"\"},instrumentType: {eq:B}}){count,data{instrumentType,instrumentVersionNbr,subject,instrumentNbr,shortTitle,createdAt,updatedAt, introducedDate, confirmedDate, actSummary,lastAction, body,introducedUrl,enrolledUrl,engrossedUrl,viewEnacted}}}","variables":{}})
response = http.request("POST", graphql_url, body=get_bill_text_and_deets_query,headers={'Content-Type': 'application/json'})
response_data = json.loads(response.data.decode('utf-8'))

#right now just overwrites any existing !!!bills!!!
for bill_act_or_other in response_data['data']['instrumentOverviews']['data']:
    try:
        bill_url=""
        #use the most recent version of the bill available
        if bill_act_or_other['enrolledUrl']:
            bill_url=bill_act_or_other['enrolledUrl']
        elif bill_act_or_other['engrossedUrl']:
            bill_url=bill_act_or_other['engrossedUrl']
        elif bill_act_or_other['introducedUrl']:
            bill_url=bill_act_or_other['introducedUrl']
        else:
            with open('bills/alabama/errors/' + bill_act_or_other['instrumentNbr'] + ".txt", "w",
                      encoding='utf-8') as file:
                file.write("No file URL Found")
            continue

        r = http.request('GET', bill_url, preload_content=False)#todo use enrolled when needed
        with open('bills/alabama/'+ bill_act_or_other['instrumentNbr']+".pdf", 'wb') as out:
            while True:
                data = r.read(1024)
                if not data:
                    break
                out.write(data)
        r.release_conn()
    except Exception as e:
        with open('bills/alabama/errors/' + bill_act_or_other['instrumentNbr'] + ".txt", "w", encoding='utf-8') as file:
            file.write(str(e))