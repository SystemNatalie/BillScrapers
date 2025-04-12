import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import json
#for using natlib
import importlib.util,sys
spec = importlib.util.spec_from_file_location("module_name", "C:\\Users\\Natalie\\PycharmProjects\\natlib\\main.py")
natlib = importlib.util.module_from_spec(spec)
sys.modules["module_name"] = natlib
spec.loader.exec_module(natlib)
#for using natlib END

http = urllib3.PoolManager()

bills=http.request('GET','https://lsoservice.wyoleg.gov/api/BillInformation?$select=*&$filter=Year%20eq%20'+str(datetime.datetime.now().year))
bills_data=json.loads(bills.data)
for bill in bills_data:
    if bill['specialSessionValue'] != None:
        bill_data = http.request('GET', "https://lsoservice.wyoleg.gov/api/BillInformation/" + str(
            datetime.datetime.now().year) + "/" + bill['billNum'] + "?specialSessionValue=1")
    else:
        bill_data = http.request('GET', "https://lsoservice.wyoleg.gov/api/BillInformation/" + str(
            datetime.datetime.now().year) + "/" + bill['billNum'] + "?specialSessionValue=null")
    if bill_data.status != 200:
        with open("bills/wyoming/error/"+bill['billNum']+".txt", "w+") as f:
            f.write("404")
        continue
    bill_data=json.loads(bill_data.data)#this has the full text of the bill but its in html format so were gonna find the pdf instead
    natlib.writeToFileStreamed("https://www.wyoleg.gov/"+bill_data['introduced'],"bills/wyoming/"+bill_data['bill']+".pdf")
