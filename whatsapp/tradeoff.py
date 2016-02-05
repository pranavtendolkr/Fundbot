import json
import requests
from requests.auth import HTTPBasicAuth

api_url = 'https://gateway.watsonplatform.net/tradeoff-analytics/api/v1/dilemmas/'
api_username = "2e32ed4f-7035-4159-9587-b88cd655f6f3"
api_password = "PHHGaNxrCLP0"
proxy = {"http": "http://bproxy.ibmsbsds1.com:3128","https": "http://bproxy.ibmsbsds1.com:3128",}


def get_listof_params(profile):
    params = []
    graph = False
    for item in profile['name_values']:
        if item['value'] is not "":
            if item['value'] == 'graph':
                graph = True
            else:
                params.append(item['value'])
    return params,graph


def call_tradeoff_api(profile):

    with open('tradeoff.json') as f:
        tradeoff_input = json.load(f)
    params,graph = get_listof_params(profile=profile)


    for param in params:
        for i, column in enumerate(tradeoff_input['columns']):
            if param == column['key']:
		print "setting %s as objective"%(tradeoff_input['columns'][i]['key'])
                tradeoff_input['columns'][i]['is_objective'] = True
    print "columns in tradeoff are\n"
    print tradeoff_input['columns']


    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(api_username,api_password)
    response = requests.post(api_url,auth=auth,headers=headers,data=json.dumps(tradeoff_input))
    # print response.status_code
    # with open('test.json','w') as f:
    #     json.dump(response.json(),f,indent=4, sort_keys=True)
    # print response.json
    if response.status_code is 200:
        return response.json(),graph
    else:
        return None,False



# profile = {
#   "name_values": [
#     {
#       "name": "param1",
#       "value": "Alpha"
#     },
#     {
#       "name": "param2",
#       "value": "Beta"
#     },
#     {
#       "name": "param3",
#       "value": "Standard Deviation"
#     },
#     {
#       "name": "param4",
#       "value": ""
#     },
#     {
#       "name": "param5",
#       "value": ""
#     },
#     {
#       "name": "param6",
#       "value": ""
#     },
#     {
#       "name": "param7",
#       "value": ""
#     },
#     {
#       "name": "param8",
#       "value": ""
#     },
#     {
#       "name": "param9",
#       "value": ""
#     },
#     {
#       "name": "param10",
#       "value": ""
#     },
#     {
#       "name": "graph",
#       "value": "graph"
#     }
#   ]
# }
#
#
# call_tradeoff_api(profile)
