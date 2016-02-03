#main dialog here

import sqlite3


# returns watson's reply
def converse(phone,message):
    # flow:
    # check user's number. get conversation id, time and client id from db
    # if not found, send blank info
    # call api
    # return response, store client id, conversation id in db

    conn = sqlite3.connect('conversations.db')
    try:
        conn.execute('''CREATE TABLE USERS
           (phone TEXT PRIMARY KEY     NOT NULL,
           conversation_id           TEXT    NOT NULL,
           client_id            TEXT     NOT NULL);''')
        print "created table"
    except Exception as e:
        print e

    query = "SELECT phone, conversation_id, client_id from USERS WHERE phone='%s';"%(phone)
    print query
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    print "db returned:"
    print rows
    if(len(rows) is 1):
        print "user found"
        conversation_id = rows[0][1]
        client_id = rows[0][2]
        print conversation_id
        print client_id
    else:
        print "user not found, sending blank data"
        conversation_id = ""
        client_id = ""

    new_client_id,new_conversation_id,response = call_api(client_id,conversation_id,message)


    # insert newly returned shit in the db
    query = '''INSERT OR REPLACE INTO USERS (phone, client_id, conversation_id) VALUES ('%s', '%s', '%s');'''%(phone,new_client_id,new_conversation_id)
    print query
    print cursor.execute(query)

    conn.commit()
    conn.close()

    return response






def call_api(client_id,conversation_id,message):
    return "new_id", "new_convo", "response1"


def get_profile(client_id):
    pass




print converse('9764210075','hi')
