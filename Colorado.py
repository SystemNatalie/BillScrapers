import urllib3
from bs4 import BeautifulSoup

#for using natlib
import importlib.util,sys
spec = importlib.util.spec_from_file_location("module_name", "C:\\Users\\Natalie\\PycharmProjects\\natlib\\main.py")
natlib = importlib.util.module_from_spec(spec)
sys.modules["module_name"] = natlib
spec.loader.exec_module(natlib)
#for using natlib END

http = urllib3.PoolManager()
init_url="https://leg.colorado.gov/"
page1="bills-by-bill-number"

response = http.request('GET', init_url+page1)
soup = BeautifulSoup(response.data, 'html.parser')
ct=0
try:
	next_page=soup.find("li", {"class": "pager-next"}).find("a").attrs["href"]
except AttributeError as e:
	next_page=None
while next_page:
	for buns in soup.find("tbody").find_all("tr"):
		bill_url= buns.find("td", {"class": "views-field-title"}).find("a").attrs["href"]
		bill_number= buns.find("td", {"class": "views-field-field-bill-number"}).text.strip()
		bill_sponsors = buns.find("td", {"class": "views-field-sponsors"})
		bill_response = http.request('GET', init_url + bill_url)
		soup2 = BeautifulSoup(bill_response.data, 'html.parser')
		doc_url=soup2.find("div", {"id": "bill-documents-tabs1"}).find("table").find("tbody").find("tr").find("a").attrs['href']#we only need the first tr so find is fine as opposed to find_all
		natlib.writeToFileStreamed(doc_url,"bills/colorado/"+bill_number+"."+doc_url.split(".")[-1])
		print(ct)
		ct+=1
	response = http.request('GET', init_url + next_page)
	soup = BeautifulSoup(response.data, 'html.parser')
	try:
		next_page = soup.find("li", {"class": "pager-next"}).find("a").attrs["href"]
	except AttributeError as e:
		next_page = None
#handle last page
for buns in soup.find("tbody").find_all("tr"):
	bill_url= buns.find("td", {"class": "views-field-title"}).find("a").attrs["href"]
	bill_number= buns.find("td", {"class": "views-field-field-bill-number"}).text.strip()
	bill_sponsors = buns.find("td", {"class": "views-field-sponsors"})
	bill_response = http.request('GET', init_url + bill_url)
	soup2 = BeautifulSoup(bill_response.data, 'html.parser')
	doc_url=soup2.find("div", {"id": "bill-documents-tabs1"}).find("table").find("tbody").find("tr").find("a").attrs['href']#we only need the first tr so find is fine as opposed to find_all
	natlib.writeToFileStreamed(doc_url,"bills/colorado/"+bill_number+"."+doc_url.split(".")[-1])
	print(ct)
	ct += 1