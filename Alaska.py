import os

import bs4.element
import urllib3

http = urllib3.PoolManager()
from bs4 import BeautifulSoup
current_session:int
getpdf=True
if getpdf:
    out_ext = "pdf"
else:
    out_ext = "txt"

r= http.request('GET', 'https://www.akleg.gov/basis/Home/Archive')
soup = BeautifulSoup(r.data, 'html.parser')
for ul in soup.find("div",{"id":"fullpage"}).find("li"):
    if type(ul) != bs4.element.Tag:
        continue
    else:
        current_session=ul.string[:2]
        break
r= http.request('GET', f'https://www.akleg.gov/basis/Bill/Range/{str(current_session)}?session=&bill1=&bill2=')
soup = BeautifulSoup(r.data, 'html.parser')
for bill in soup.find_all("td",{"class":"billRoot"}):
    link=bill.find("a").string
    r2= http.request('GET', f'https://www.akleg.gov/basis/Bill/Detail/{str(current_session)}?Root={link}')
    soup2 = BeautifulSoup(r2.data, 'html.parser')
    tables=soup2.find("div",{"id":"tab1_4"})
    try:
        if getpdf:
            download_url = tables.find("tbody").find_all("a",{"class":"pdf"})[-1]['href']
        else:
            download_url = "https://www.akleg.gov"+tables.find("tbody").find("td",{"data-label":"Version"}).find("a")['href']

        if not os.path.exists("bills/alaska/"+link+f".{out_ext}"): #TODO allow overriding of this
            r2 = http.request('GET', download_url, preload_content=False)
            if not getpdf:#do extra processing for direct txt
                outData=""
                soup2 = BeautifulSoup(r2.data, 'html.parser')
                bill_text=soup2.find_all("p",{"class":"tighter"})
                for bill_part in bill_text:
                    t = bill_part.text
                    outData+=t
                with open('bills/alaska/' + link + f".{out_ext}", 'w') as out:
                        out.write(outData)
            else:
                with open('bills/alaska/' + link + f".{out_ext}", 'wb') as out:
                    while True:
                        data = r2.read(1024)
                        if not data:
                            break
                        out.write(data)
                r2.release_conn()
    except Exception as e:
        if type(e) == IndexError:
            error_string = "No Download PDF Found"
        else:
            error_string = str(e)
        with open('bills/alaska/errors/' + link + ".txt", 'w') as out:
            out.write(error_string)
        continue