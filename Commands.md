# Mongodb Commands:
-------------------

db.help()
show dbs
use dbname
show collections
show users
db.dropDatabase()
db.collection.find()
db.collection.insertOne()
db.collection.drop()
------------------------------------------------------------------------------
# Kafka Commands:
----------------

#To start Zookeeper
.\bin\windows\zookeeper-server-start.bat config\zookeeper.properties

#To start kafka server
.\bin\windows\kafka-server-start.bat config\server.properties

#To create a topic
.\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test


#To list the topics
.\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092


#For Console Producer
.\bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test

#For Console Consumer
.\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning


------------------------------------------------------------------------------

