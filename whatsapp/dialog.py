#main dialog here

import sqlite3
import datetime
from dateutil import parser
import random

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
           client_id            TEXT     NOT NULL,
           convo_time timestamp NOT NULL );''')
        print "created table"
    except Exception as e:
        print e

    query = "SELECT phone, conversation_id, client_id,convo_time from USERS WHERE phone='%s';"%(phone)
    print query
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    print "db returned:"
    print rows
    if(len(rows) is 1):
        print "user found"
        conversation_id = rows[0][1]
        client_id = rows[0][2]
        convo_time = parser.parse(rows[0][3])
        print conversation_id
        print client_id
    else:
        print "user not found, sending blank data"
        conversation_id = ""
        client_id = ""
        convo_time=datetime.datetime.utcfromtimestamp(0)

    #check if the convo has expired.
    # consversations expire if last msg time is more than 15 min
    elapsed = datetime.datetime.now() - convo_time
    if elapsed > datetime.timedelta(minutes=15):
        print "expiring consversations id"
        conversation_id = ""



    new_client_id,new_conversation_id,response = call_api(client_id,conversation_id,message)

    # insert newly returned data in the db
    query = '''INSERT OR REPLACE INTO USERS (phone, client_id, conversation_id,convo_time) VALUES ('%s', '%s', '%s','%s');'''%(phone,new_client_id,new_conversation_id, datetime.datetime.now())
    #query = '''INSERT OR REPLACE INTO USERS (phone, client_id, conversation_id,convo_time) VALUES (, '%s', '%s','%s');'''%(phone,new_client_id,new_conversation_id, datetime.datetime.now())
    print query
    print cursor.execute(query)

    conn.commit()
    conn.close()


    return response






def call_api(client_id,conversation_id,message):
    return random.random(), random.random() , "response1"


def get_profile(client_id):
    pass




print converse('97642100075','hi')
