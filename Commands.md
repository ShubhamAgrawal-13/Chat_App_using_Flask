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
#Kafka Commands:
----------------

#To start Zookeeper
.\bin\windows\zookeeper-server-start config\zookeeper.properties

#To start kafka server
.\bin\windows\kafka-server-start config\server.properties

#To create a topic
.\bin\windows\kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test


#To list the topics
.\bin\windows\kafka-topics.sh --list --bootstrap-server localhost:9092


#For Console Producer
.\bin\windows\kafka-console-producer.sh --broker-list localhost:9092 --topic test

#For Console Consumer
.\bin\windows\kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning


------------------------------------------------------------------------------

