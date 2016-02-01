import json

def get_values(data):

    values = []
    i = 1
    for item in data:
        option = {}
        option['key'] = i
        option['name'] = item['Fund']
        option['description_html'] =  '%s (%s)'%(item['Fund'],item['Capitalisation'])
        option['values'] = item
        option['app_data'] = {}
        values.append(option)
        i = i+1
    return values
    # with open('tradeoff.json','w') as f:
    #     json.dump(values,f,sort_keys=True,indent=4, separators=(',', ': '))

def normalize_data(data):
    for item in data:
        item['Rating'] = item['Rating'].count('*')
        if item['Fund Risk Grade'] == 'High':
            item['Fund Risk Grade'] = 5
        elif item['Fund Risk Grade'] == 'Above Average':
            item['Fund Risk Grade'] = 4
        elif item['Fund Risk Grade'] == 'Average':
            item['Fund Risk Grade'] = 3
        elif item['Fund Risk Grade'] == 'Below Average':
            item['Fund Risk Grade'] = 2
        elif item['Fund Risk Grade'] == 'Low':
            item['Fund Risk Grade'] = 1
        else:
            item['Fund Risk Grade'] = 3
    return data

def get_columns():
    pass

with open('funds.json') as f:
    data = json.load(f)

data = normalize_data(data)
values = get_values(data=data)
print json.dumps(values,sort_keys=True,indent=4, separators=(',', ': '))
