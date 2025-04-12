import urllib3
import os
from bs4 import BeautifulSoup
http = urllib3.PoolManager()

#Originally for when we needed to get the session, however we're just assuming that https://www.azleg.gov/bills/
# gives us the most recent each time.
"""arizona_leg_home_url="https://www.azleg.gov/"
headers= {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Referer": "https://www.azleg.gov/azlegwp/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }
response = http.request("GET", arizona_leg_home_url,headers=headers)
soup = BeautifulSoup(response.data, 'html.parser')
sessions=soup.find("select", {"class":"selectSession"})
session_id=-1
for opt in sessions:
    session_id = opt.attrs["value"]
    break
if session_id != -1:
    raise Exception("Failed to find current session.")
"""

az_bills_url = "https://www.azleg.gov/bills/"
headers= {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
	"Referer": "https://www.azleg.gov/azlegwp/",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
}
response = http.request("GET", az_bills_url,headers=headers)
soup = BeautifulSoup(response.data, 'html.parser')
bills=soup.find_all("a", {"class":"faqLink"})
bill_doc_url = "https://apps.azleg.gov/api/DocType/?billStatusId="
html_path="Error"
#TODO further hangle exceptions
for bill in bills:
	bill_number = bill.string
	if os.path.exists("./bills/arizona/"+bill_number+".htm"): #todo add redownload flag
		continue
	sub_response = http.request("GET", bill_doc_url+bill['href'].split("/")[-1], headers=headers)
	soup2 = BeautifulSoup(sub_response.data, 'html.parser')
	bv = soup2.find("documents") #NOTE The website returns this using caps (LikeThis) but for some fucking reason
	#it doesnt want to work unless i dont utilize caps
	#This is a consistent issue seen when dealing with any xml, and is not solved by switching the parser to lxml
	try:
		for bill_version in bv.find_all("strdocumentmodel"):
			html_path=bill_version.find("htmlpath").string
	except Exception as e:
		with open('bills/arizona/errors/' + bill_number + ".txt", "w", encoding='utf-8') as file:
			file.write(str(e))
			continue
	try:
		r = http.request('GET', html_path,headers=headers, preload_content=False)
		with open('bills/arizona/'+bill_number+".htm", 'wb') as out:
			while True:
				data = r.read(1024)
				if not data:
					break
				out.write(data)
		r.release_conn()
	except Exception as e:
		with open('bills/arizona/errors/' +bill_number+ ".txt", "w", encoding='utf-8') as file:
			file.write(str(e))

#house_bill_table=soup.find("div",{"name":"HBTable"})
#senate_bill_table=soup.find("div",{"name":"SBTable"})
#todo remove memorials and resolutions

#tabs = house_bill_table.find_all("div",{"role":"tablist"})
#for tab in tabs:
#    tab_items = tab.find("tbody").find_all("tr")
#    for tab_item in tab_items:
#        link = tab_item.find("th").find("a")
#        print("ya mama")