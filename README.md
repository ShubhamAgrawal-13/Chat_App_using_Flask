## Objective
-------------
To make a chat app using flask:
1. Register user
2. Login user 
3. Send Message
4. Deleting/ Updating messages
5. Should support group chat
6. chat should be persistent
------------------------------------------------------------------------------
# First we will try to create a flask app.

# Html Pages:
home
login
register
dashboard

-------------------------------------------------------------------------------
# How we will store the user information?

```
{
    "user1" : {

            "cid" : "user2",
            "user_list" : ["user2", "user3"],
            "group_list" : ["group1"],
            "msg_list" : {
                            "user2":{
                                 "1":{
                                    "sender_uid": "user2",
                                    "text": "Hi",
                                    "timestamp": "11:20 am"

                                },
                                  "2":{
                                    "sender_uid": "user3",
                                    "text": "Hi, user1",
                                    "timestamp": "11:24 am"

                                }
                            }
                           
                         }

            },
    "user2" : {

            "cid" : "user2",
            "user_list" : ["user1", "user3"],
            "group_list" : ["group1"],
            "msg_list" : {
                              "user1":{
                                 "3":{
                                    "sender_uid": "user2",
                                    "text": "Hi",
                                    "timestamp": "11:20 am"

                                    },
                                "2":{
                                    "sender_uid": "user3",
                                    "text": "Hi, user1",
                                    "timestamp": "11:24 am"

                                    }
                                  }
                            
                         }

            }
}
```


----------------------------------------------------------------------------
# register form and login form css
button {
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 30%;
}

button:hover {
  opacity: 0.8;
}

input[type=text], input[type=password], input[type=email]  {   
  width: 100%;   
  margin: 8px 0;  
  padding: 12px 20px;   
  display: inline-block;   
  border: 2px solid green;   
  box-sizing: border-box;   
} 

-------------------------------------------------------------------------------

Database Connection:
--------------------

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = myclient["authentication"]
user_table = user_db["user_info"]

if(request.method == 'POST'):
    req = request.form
    req = dict(req)

#insert a record
user_table.insert_one(reg_dict)

#query a record
query = user_table.find({'uid':req['uid']})

-------------------------------------------------------------------------------

#User Record
"""
{ User Info Table}

{
    {
        "user_id": message['uid'],
        "email": message['email'], 
        "password": message['password']
    }
}

"""

------------------------------------------------------------------------------
# Producer:

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
producer.send(topic, json.dumps(dict_msg).encode('utf-8'))


# Consumer
consumer = KafkaConsumer(user_id,
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='latest',
         enable_auto_commit=True,
         value_deserializer=lambda x: loads(x.decode('utf-8')))
    
for msg in consumer:
    print(msg.value)

--------------------------------------------------------------------------------

<script>
    chatWindow = document.getElementById('chat_window'); 
    var xH = chatWindow.scrollHeight; 
    chatWindow.scrollTo(0, xH);
</script>

--------------------------------------------------------------------------------

onClick="window.location.reload();"

--------------------------------------------------------------------------------

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["GlobalDB"]

--------------------------------------------------------------------------------
<script>
    function openDiv() {
      document.getElementById("div").style.display = "block";
    }

    function closeDiv() {
      document.getElementById("div").style.display = "none";
    }
</script>
--------------------------------------------------------------------------------
Update Msg:
-----------
mycol = mydb[collection_name]
myquery = { "msg_id": msg_id }
mydoc = mycol.find(myquery)
newvalues = { "$set": { "text": text } }
mycol.update_one(myquery, newvalues)
---------------------------------------------------------------------------------
Delete Msg:
-----------
mycol = mydb[collection_name]
myquery = { "msg_id": msg_id }
mydoc = mycol.find(myquery)
for x in mydoc:
    mycol.delete_one(x)
---------------------------------------------------------------------------------