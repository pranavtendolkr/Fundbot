import json

# dumps data from  valueresearchonline into a compatible format frr tradeoff analysis
# creates tradeoff.json in the current directory



#columns we can include
            # "1-Year Return (%)": "-15.25",
            # "Alpha": "6.62",
            # "Beta": "1.05",
            # "Expense Ratio (%)": "2.61",
            # "Fund Risk Grade": "5",
            # "Launch": "Feb 24, 2004",
            # "Market Cap": "42956.99",
            # "Net Assets (Cr)": "536.08",
            # "R-Squared": "0.87",
            # "Rating": "3",
            # "Sharpe Ratio": "0.71",
            # "Sortino Ratio": "1.37",
            # "Standard Deviation": "15.26",
            # "Turnover": "35"

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
    #the dirtiest method in the code.
    for item in data:
        #convert rating to
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


        item['Rating'] = int(item['Rating'])

        # convert string values to floats
        columns = ['1-Year Return (%)','Alpha','Beta','Expense Ratio (%)',
                   'Fund Risk Grade','Market Cap','Net Assets (Cr)',
                   'R-Squared','Sharpe Ratio','Sortino Ratio','Standard Deviation','Turnover']

        for column in columns:
            try:
                item[column] = float(item[column])
            except Exception as e:
                print '%s is invalid in %s' %(column, item['Fund'])
                item[column] = 0.0

    return data

def get_columns(objectives):
    # i have no idea what i am doing.
    fields = ['1-Year Return (%)','Alpha','Beta','Expense Ratio (%)',
                   'Fund Risk Grade','Market Cap','Net Assets (Cr)',
                   'R-Squared','Sharpe Ratio','Sortino Ratio','Standard Deviation','Turnover']
    # these fields will be maximized, rest all minimized
    max_fields = ['1-Year Return (%)','Alpha','Market Cap',
                 'Net Assets (Cr)','Sharpe Ratio','Sortino Ratio','Turnover']

    # min_fields = ['Beta','Expense Ratio (%)','Fund Risk Grade','R-Squared','Standard Deviation',]

    columns = []

    for field in fields:
        column = {}
        column["type"] = 'numeric'
        column["key"] = field
        if field in max_fields:
            column["goal"] = 'max'
        else:
            column["goal"] = 'min'
        column["full_name"] = field
        if field in objectives:
            column["is_objective"] = True
        columns.append(column)

    return columns

# with open('funds.json') as f:
#     data = json.load(f)

import mf_data as crawler

data = crawler.crawl_data()

data = normalize_data(data)
values = get_values(data=data)
columns = get_columns(objectives=['Fund Risk Grade','Market Cap','Net Assets (Cr)','Sortino Ratio'])

alldata = {}
alldata['subject'] = "mutual funds"
alldata['columns'] = columns
alldata['options'] = values

# problem = {}
# problem["problem"] = alldata


with open('tradeoff.json','w') as f:
    json.dump(alldata,f,sort_keys=True,indent=4, separators=(',', ': '))
