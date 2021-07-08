# Chat App using Flask
------------------------------------------------------------------------------
# Objective:
------------------------------------------------------------------------------
To make a chat app using flask:
1. Register user
2. Login user 
3. Send Message
4. Deleting/ Updating messages
5. Should support group chat
6. Chats should be persistent
------------------------------------------------------------------------------
# Overall Flow:
![Flow](images/Flow.png)
------------------------------------------------------------------------------
# Dashboard:
![Dashboard](images/Dashboard.png)
------------------------------------------------------------------------------
# How to run the code?

1. **Start Zookeeper :** First go to the directory where the kafka is present, then the run the following command:
```
.\bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

2. **Start Kafka Server:** Run the following command:
```
.\bin\windows\kafka-server-start.bat config\server.properties
```

3. **Start Flask Server:** First go to the Chat App directory, then the run the following command:
```
python home.py
```

4. **Start Action Server:** Run the following command:
```
python action_server.py
```

------------------------------------------------------------------------------
## Files:

### Html Pages(templates directory):
1. home.html
2. login.html
3. register.html
4. dashboard.html
5. invalid.html

### Python Files:
1. home.py
2. action_server.py


### static files(static directory):
1. styles.css

### Info files:
1. msg_id.txt
2. users.txt
3. groups.txt
4. group_mapping.txt 

-------------------------------------------------------------------------------
# How we will store the user information?
## User Record
```
{ User Info Table}

{
    {
        "user_id": message['uid'],
        "email": message['email'], 
        "password": message['password']
    }
}
```

## Users Data

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
# Database Connection (MongoDB)

```
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = myclient["authentication"]
user_table = user_db["user_info"]
```

## Insert a record
`user_table.insert_one(reg_dict)`

## Query a record
`query = user_table.find({'uid':req['uid']})`

```
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["GlobalDB"]
```

## Update a record
```
mycol = mydb[collection_name]
myquery = { "msg_id": msg_id }
mydoc = mycol.find(myquery)
newvalues = { "$set": { "text": text } }
mycol.update_one(myquery, newvalues)
```

## Delete a record
```
mycol = mydb[collection_name]
myquery = { "msg_id": msg_id }
mydoc = mycol.find(myquery)
for x in mydoc:
    mycol.delete_one(x)
```

------------------------------------------------------------------------------
# Kafka 
## Producer Object in python:

```
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
producer.send(topic, json.dumps(dict_msg).encode('utf-8'))
```

## Consumer Object in python:
```
consumer = KafkaConsumer(user_id,
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='latest',
         enable_auto_commit=True,
         value_deserializer=lambda x: loads(x.decode('utf-8')))
    
for msg in consumer:
    print(msg.value)
```
-------------------------------------------------------------------------------
# JavaScript:

```
<script>
    chatWindow = document.getElementById('chat_window'); 
    var xH = chatWindow.scrollHeight; 
    chatWindow.scrollTo(0, xH);
</script>

onClick="window.location.reload();

<script>
    function openDiv() {
      document.getElementById("div").style.display = "block";
    }

    function closeDiv() {
      document.getElementById("div").style.display = "none";
    }
</script>

```
------------------------------------------------------------------------------