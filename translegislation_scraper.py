import urllib3
import datetime
import json
import base64
import bs4 as BeautifulSoup
"""
Scrapes the TransLegislation website, very useful for getting positive bill definitions to initially train
our model with.
"""

http = urllib3.PoolManager()

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
              'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
              'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC',
              'US']  # states + DC,and US..  were going to use the congress.gov api
state_url_prefix = "https://translegislation.com/bills/"+str(datetime.datetime.now().year)+"/"
for state in states:
	response = http.request('GET', state_url_prefix+state)
	soup = BeautifulSoup.BeautifulSoup(response.data, features="html.parser")
	json_bills_for_state = json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).text)
	bills= json_bills_for_state['props']['pageProps']['bills']
	for bill in bills:
		bill_response = http.request('GET', state_url_prefix + bill['state']+"/"+bill['bill_number'])
		soup2 = BeautifulSoup.BeautifulSoup(bill_response.data, features="html.parser")
		json_bill=json.loads(soup2.find("script", {"id": "__NEXT_DATA__"}).text)
		try:
			bill_text_type=json_bill['props']['pageProps']['bill']['bill_text']['type']
			bill_text=json_bill['props']['pageProps']['bill']['bill_text']['content']
			if bill_text_type=='pdf':
				base64_string = bill_text[len('data:application/pdf;base64,'):]
				pdf_bytes = base64.b64decode(base64_string)
				with open("translegislation_bills/"+json_bill['props']['pageProps']['bill']['state']+"-"+json_bill['props']['pageProps']['bill']['bill_number']+".pdf", 'wb') as pdf_file:
					pdf_file.write(pdf_bytes)
			else:
				print(bill_text_type)
		except Exception as e:
			with open("translegislation_bills/error/" + json_bill['props']['pageProps']['bill']['state'] + "-" + json_bill['props']['pageProps']['bill']['bill_number'] + ".txt", 'w+') as pdf_file:
				pdf_file.write(str(e))
