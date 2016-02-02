# crawls valueresearchonline for mutual fund data


import requests
import string
import csv
import json



Login_URL = 'https://www.valueresearchonline.com/registration/loginprocess.asp'
proxy = {"http": "http://bproxy.ibmsbsds1.com:3128","https": "http://bproxy.ibmsbsds1.com:3128",}
#base_url = 'https://www.valueresearchonline.com/funds/fundSelector/fundSelectResult.asp?cat=&exc=&schemecode=&myport=&pg=&fType=csv&funcName='
base_url = 'https://www.valueresearchonline.com/funds/fundSelector/fundSelectResult.asp?cat=&exc=fmp,susp,dir,close&schemecode=&myport=&pg=&fType=csv&funcName='

topics = ['portfolio','returns','snapshot','risk','navdetails','fees']

creds = {
    'username': 'someonesomeone@mailinator.com',
    'password': 'Aq1sw2de'
    }

#  crawls valueresearchonline for mutual fund data and returns a list of dictionaries
def crawl_data():
    with requests.Session() as s:
        p = s.post(Login_URL, data=creds, proxies=proxy)
        topicData = []
        for topic in topics:
            url = base_url + topic
            r = s.get(url,proxies=proxy)
            data = r.text.split('\r')[2:]
            result = csv.DictReader(data)
            topicData.append(list(result))

        for company in topicData[0]:
            #print company
            for i in range(1,5):
                #print i
                for row in topicData[i]:
                    if i == 4:
                        if company['Fund'] == row['Scheme']:
                            company.update(row)
                    else:
                        if company['Fund'] == row['Fund']:
                            company.update(row)


        # with open('funds.json','w') as f:
        #     json.dump(topicData[0],f)
        return topicData[0]
