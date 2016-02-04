import rest_call

conversation_id = ""
client_id = ""
message="hi"
param = {'client_id': client_id, 'conversation_id':conversation_id, 'input':message}

res = rest_call.post_request('conversation',param)
print(res['response'])
print(res['client_id'])
print(res['conversation_id'])
print('---------------------')

conversation_id = res['conversation_id']
client_id = res['client_id']
message="which"
param = {'client_id': client_id, 'conversation_id':conversation_id, 'input':message}

res = rest_call.post_request('conversation',param)

print(res['response'])
print(res['client_id'])
print(res['conversation_id'])
print('---------------------')



conversation_id = res['conversation_id']
client_id = res['client_id']
message="Beta, Alpha, Standard Deviation, Sharpe Ratio"
param = {'client_id': client_id, 'conversation_id':conversation_id, 'input':message}

res = rest_call.post_request('conversation',param)

print(res['response'])
print(res['client_id'])
print(res['conversation_id'])
print('---------------------')
conversation_id = res['conversation_id']
client_id = res['client_id']
message="yes"
param = {'client_id': client_id, 'conversation_id':conversation_id, 'input':message}

res = rest_call.post_request('conversation',param)

print(res['response'])
print(res['client_id'])
print(res['conversation_id'])
print('---------------------')

conversation_id = res['conversation_id']
client_id = res['client_id']
message="yes"
param = {'client_id': client_id, 'conversation_id':conversation_id, 'input':message}

res = rest_call.post_request('conversation',param)
print(res)
print(res['response'])
print(res['client_id'])
print(res['conversation_id'])
print('---------------------')

client_id = res['client_id']
param = {'client_id': client_id}
res = rest_call.get_request('profile',param)

for i in res['name_values']:
    print(i)