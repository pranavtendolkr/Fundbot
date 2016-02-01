import requests
import string
import csv
import json

proxy = {"http": "http://bproxy.ibmsbsds1.com:3128","https": "http://bproxy.ibmsbsds1.com:3128",}

Login_URL = 'https://www.valueresearchonline.com/registration/loginprocess.asp'

overview = 'https://www.valueresearchonline.com/stocks/StockSelector/StockSelectResult.asp?funcName=snapshot&index=&cap=&sec=&indus=&myport=&fType=csv&firstchar='
essential_checks = 'https://www.valueresearchonline.com/stocks/StockSelector/StockSelectResult.asp?funcName=essential_checks&index=&cap=&sec=&indus=&myport=&fType=csv&firstchar='
returns = 'https://www.valueresearchonline.com/stocks/StockSelector/StockSelectResult.asp?funcName=returns&index=&cap=&sec=&indus=&myport=&fType=csv&firstchar='
health = 'https://www.valueresearchonline.com/stocks/StockSelector/StockSelectResult.asp?funcName=financial_health&index=&cap=&sec=&indus=&myport=&fType=csv&firstchar='
growth = 'https://www.valueresearchonline.com/stocks/StockSelector/StockSelectResult.asp?funcName=growth&index=&cap=&sec=&indus=&myport=&fType=csv&firstchar='

topics = [overview,essential_checks,returns,health,growth]

creds = {
    'username': 'someonesomeone@mailinator.com',
    'password': 'Aq1sw2de'
    }


with requests.Session() as s:
    p = s.post(Login_URL, data=creds, proxies=proxy)
    all_data=[]
    for letter in string.uppercase + '2378':
        topicData = []
        for topic in topics:
            url = topic+letter
            r = s.get(url,proxies=proxy)
            data = r.text.split('\r')[2:]
            result = csv.DictReader(data)
            topicData.append(list(result))

        for company in topicData[0]:
            for row in topicData[1]:
                if company['Company'] == row['Company']:
                    print row['Company']
                    company.update(row)
            for row in topicData[2]:
                if company['Company'] == row['Company']:
                    print row['Company']
                    company.update(row)
            for row in topicData[3]:
                if company['Company'] == row['Company']:
                    print row['Company']
                    company.update(row)
            for row in topicData[4]:
                if company['Company'] == row['Company']:
                    print row['Company']
                    company.update(row)
        all_data = all_data + topicData[0]

    with open('data.json','w') as f:
        json.dump(all_data,f)
