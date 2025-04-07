#todo kinda slow, may need to update to be multithreaded or something
import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
response=http.request("GET","https://leginfo.legislature.ca.gov/faces/billSearchClient.xhtml")
soup= BeautifulSoup(response.data, 'html.parser')
session_years = soup.find("select",{"id":"session_year"}).find("option").attrs["value"]
print("got session")
bills_url=f'https://leginfo.legislature.ca.gov/faces/billSearchClient.xhtml?session_year={session_years}'
response=http.request("GET",bills_url)
soup = BeautifulSoup(response.data, 'html.parser')
bills_table=soup.find("table",{"id":"bill_results"}).find("tbody")
bill_final_url="https://leginfo.legislature.ca.gov"
ct=0
for row in bills_table.find_all("tr"):
	link=row.find("a")
	bill_data_response = http.request("GET", bill_final_url+link.attrs["href"])
	bill_soup = BeautifulSoup(bill_data_response.data, 'html.parser')
	bill_dat=bill_soup.find("div",{"id":"bill_all"})
	with open("bills/california/"+link.text.strip()+".html",'w+', encoding='utf-8') as f:
		f.write(bill_dat.prettify())
	print("got bill: "+str(ct))
	ct+=1