import requests
import json
from requests.auth import HTTPBasicAuth

dialog_id = 'c6d5a75f-6630-4869-967e-1e1b4d036b54'
URL = 'https://gateway.watsonplatform.net/dialog/api/v1/dialogs/{0}/{1}'

#proxy = {"http": "http://bproxy.ibmsbsds1.com:3128","https": "http://bproxy.ibmsbsds1.com:3128",}
#proxy = {"http": "http://yussuf_shaikh:C##mel0nt0p@goaproxy.persistent.co.in:8080","https": "http://yussuf_shaikh:C##mel0nt0p@goaproxy.persistent.co.in:8080",}
#proxy = {"http": "http://localhost:3128", "https": "http://localhost:3128",}

creds = {
    'username': 'f30f3952-5138-40a0-958c-878f1e95a0f1',
    'password': 'MJ8fjsSjeMlb'
    }

def post_request(path,param):
    login_URL = URL
    login_URL = login_URL.format(dialog_id, path)

    p = requests.post(login_URL, auth=HTTPBasicAuth(creds['username'], creds['password']), params=param )
    #p = requests.post(login_URL, auth=HTTPBasicAuth(creds['username'], creds['password']), proxies=proxy, params=param )
    if p.status_code == 201 or p.status_code == 200:
        return p.json()
    else:
        print(p.text)
        return "Sorry, Something went wrong!!!"



def get_request(path,param):

    login_URL = URL
    login_URL = login_URL.format(dialog_id, path)
    query=''
    for key in param:
        query=query+"{0}={1}".format(key,param[key])+"&"

    login_URL = login_URL +'?'+query

    print(login_URL)
    # p = requests.get(login_URL, auth=HTTPBasicAuth(creds['username'], creds['password']), proxies=proxy)
    p = requests.get(login_URL, auth=HTTPBasicAuth(creds['username'], creds['password']))
    if p.status_code == 201 or p.status_code == 200:
        return p.json()
    else:
        print(p.text)
        return "Sorry, Something went wrong!!!"
