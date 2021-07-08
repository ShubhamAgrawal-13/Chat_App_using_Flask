from flask import Flask, render_template, url_for, request, redirect  
from kafka import KafkaConsumer
from kafka import KafkaProducer
import os
import time
import json
import pymongo
import datetime
from json import loads, dumps
import threading


app = Flask(__name__)
app.secret_key = 'any random string'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = myclient["authentication"]
user_table = user_db["user_info"]

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

users_data = {}
msg_count = 0
file = open("msg_id.txt", "r")
msg_count = int(str(file.readline().strip()))
file.close()

def user_handle(user_id):
	global users_data
	consumer = KafkaConsumer(user_id,
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='latest',
         enable_auto_commit=True,
         value_deserializer=lambda x: loads(x.decode('utf-8')))
    
	for msg in consumer:
	    print(msg.value)
	    rec_dict = msg.value
	    if user_id in users_data:
	    	print(user_id, " Entered")
	    	if(rec_dict["op_type"] == "send"):
	    		msg_id = rec_dict["msg_id"]
	    		uid1 = rec_dict["uid1"]
	    		uid2 = rec_dict["uid2"]
	    		if uid1 not in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid1] = {}

	    		users_data[user_id]["msg_list"][uid1][msg_id] = {}
	    		users_data[user_id]["msg_list"][uid1][msg_id]["text"] = rec_dict["text"]
	    		users_data[user_id]["msg_list"][uid1][msg_id]["timestamp"] = rec_dict["timestamp"]
	    		users_data[user_id]["msg_list"][uid1][msg_id]["send_uid"] = uid1

	    	elif(rec_dict["op_type"] == "fetch_msgs"):
	    		uid1 = rec_dict['uid1']
	    		uid2 = rec_dict['uid2']
	    		messages = rec_dict['messages']
	    		if uid2 not in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid2] = {}

	    		for msg in messages:
	    			msg_id = msg['msg_id']
	    			users_data[user_id]["msg_list"][uid2][msg_id] = {}
	    			users_data[user_id]["msg_list"][uid2][msg_id]["text"] = msg["text"]
	    			users_data[user_id]["msg_list"][uid2][msg_id]["timestamp"] = msg["timestamp"]
	    			users_data[user_id]["msg_list"][uid2][msg_id]["send_uid"] = msg["send_uid"]

	    	elif(rec_dict["op_type"] == "grp_send"):
	    		msg_id = rec_dict["msg_id"]
	    		uid1 = rec_dict["uid1"]
	    		uid2 = rec_dict["uid2"]
	    		if uid2 not in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid2] = {}

	    		users_data[user_id]["msg_list"][uid2][msg_id] = {}
	    		users_data[user_id]["msg_list"][uid2][msg_id]["text"] = rec_dict["text"]
	    		users_data[user_id]["msg_list"][uid2][msg_id]["timestamp"] = rec_dict["timestamp"]
	    		users_data[user_id]["msg_list"][uid2][msg_id]["send_uid"] = uid1

	    	elif(rec_dict["op_type"] == "update_msg"):
	    		msg_id = rec_dict["msg_id"]
	    		uid1 = rec_dict["uid1"]
	    		uid2 = rec_dict["uid2"]
	    		if uid1 in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid1][msg_id] = {}
	    			users_data[user_id]["msg_list"][uid1][msg_id]["text"] = rec_dict["text"]
	    			users_data[user_id]["msg_list"][uid1][msg_id]["timestamp"] = rec_dict["timestamp"]
	    			users_data[user_id]["msg_list"][uid1][msg_id]["send_uid"] = uid1

	    	elif(rec_dict["op_type"] == "delete_msg"):
	    		msg_id = rec_dict["msg_id"]
	    		uid1 = rec_dict["uid1"]
	    		uid2 = rec_dict["uid2"]
	    		if uid1 in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid1].pop(msg_id)

	    	elif(rec_dict["op_type"] == "grp_update"):
	    		msg_id = rec_dict["msg_id"]
	    		uid1 = rec_dict["uid1"]
	    		uid2 = rec_dict["uid2"]
	    		if uid2 in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid2][msg_id] = {}
	    			users_data[user_id]["msg_list"][uid2][msg_id]["text"] = rec_dict["text"]
	    			users_data[user_id]["msg_list"][uid2][msg_id]["timestamp"] = rec_dict["timestamp"]
	    			users_data[user_id]["msg_list"][uid2][msg_id]["send_uid"] = uid1

	    	elif(rec_dict["op_type"] == "grp_delete"):
	    		msg_id = rec_dict["msg_id"]
	    		uid1 = rec_dict["uid1"]
	    		uid2 = rec_dict["uid2"]
	    		if uid2 in users_data[user_id]["msg_list"]:
	    			users_data[user_id]["msg_list"][uid2].pop(msg_id)



@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
	return render_template("register.html")

@app.route("/register_check", methods=['GET', 'POST'])
def register_check():
	global users_data
	if(request.method == 'POST'):
		req = request.form
		req = dict(req)
		print(req)
		query = user_table.find({'uid':req['uid']})
		flag = 0
		for x in query:
			if(x['uid'] == req['uid']):
				flag=1
				break

		reg_dict = {
			"uid": req['uid'],
			"email" : req['email'],
			"password" : req['password']
		}

		if(flag==0):
			temp = user_table.insert_one(reg_dict)
			uid = req['uid']
			users_data[uid] = {}
			users_data[uid]['cid'] = None
			users_data[uid]['user_list'] = []
			users_data[uid]['group_list'] = []
			users_data[uid]['msg_list'] = {}

			t1 = threading.Thread(target=user_handle, args=(uid, ))
			t1.start()
			return redirect('/dashboard/'+str(uid))
		else:
			return render_template("invalid.html", message = "User already registered")
		
	return render_template("register.html")

@app.route("/login",  methods=['GET', 'POST'])
def login():
	return render_template("login.html")

@app.route("/login_check", methods=['GET', 'POST'])
def login_check():
	global users_data
	if(request.method == 'POST'):
		req = request.form
		req = dict(req)
		print(req)
		query = user_table.find({'uid':req['uid']})
		flag = 0
		temp = None
		for x in query:
			if(x['uid'] == req['uid']):
				flag=1
				temp = x
				break

		if(flag==1):
			if(temp['password'] == req['password']):
				uid = req['uid']
				users_data[uid] = {}
				users_data[uid]['cid'] = None
				users_data[uid]['user_list'] = []
				users_data[uid]['group_list'] = []
				users_data[uid]['msg_list'] = {}
				t1 = threading.Thread(target=user_handle, args=(uid, ))
				t1.start()
				return redirect('/dashboard/'+str(uid))
			else:
				return render_template("invalid.html", message="incorrect password")
		else:
			return render_template("invalid.html", message="user not registered")


	return render_template("login.html")


@app.route("/fetch_user/<string:user_id>", methods=['GET', 'POST'])
def fetch_user(user_id):
	global users_data
	file = open("users.txt", "r")
	data = file.readlines()
	users_data[user_id]['user_list'] = data
	return redirect("/dashboard/"+str(user_id))

@app.route("/fetch_group/<string:user_id>", methods=['GET', 'POST'])
def fetch_group(user_id):
	global users_data
	file = open("groups.txt", "r")
	data = file.readlines()
	users_data[user_id]['group_list'] = data
	return redirect("/dashboard/"+str(user_id))

@app.route('/update_cid/<string:user_id>/<string:chat_id>', methods = ['GET', 'POST'])
def update_cid(user_id, chat_id):
	global users_data
	users_data[user_id]['cid'] = chat_id
	return redirect('/dashboard/'+str(user_id))

@app.route("/dashboard/<string:user_id>",  methods=['GET', 'POST'])
def dashboard(user_id):
	global users_data
	chat_id = users_data[user_id]['cid']
	if chat_id != None:
		chat_id = chat_id.strip() 

	if user_id in users_data:
		if chat_id in users_data[user_id]['msg_list']:
			return render_template("dashboard.html",
								uid = user_id,
								cid = users_data[user_id]['cid'],
								user_list = users_data[user_id]['user_list'],
								group_list = users_data[user_id]['group_list'],
								msg_list = users_data[user_id]['msg_list'][chat_id])
		else:
			return render_template("dashboard.html",
								uid = user_id,
								cid = users_data[user_id]['cid'],
								user_list = users_data[user_id]['user_list'],
								group_list = users_data[user_id]['group_list'],
								msg_list = {})

	return redirect("/home")

@app.route("/send_msg/<string:user_id>", methods=['GET', 'POST'])
def send_msg(user_id):
	global users_data, msg_count, producer
	if (request.method == 'POST'):
		req = request.form
		req = dict(req)
		print(req)
		text = req['typed_msg']
		chat_id = users_data[user_id]['cid']
		if chat_id != None:
			chat_id = chat_id.strip() 
		msg_count +=1
		file = open("msg_id.txt", "w")
		file.write(str(msg_count))
		file.close()
		msg_id = str(msg_count)
		timestamp = str(datetime.datetime.now())

		dict_msg = {
			"op_type":"send",
			"uid1":user_id,
			"uid2":chat_id,
			"text":text,
			"timestamp":timestamp,
			"msg_id":msg_id
		}

		topic = "ActionServer"
		producer.send(topic, json.dumps(dict_msg).encode('utf-8'))

		if chat_id in users_data[user_id]['msg_list']:
			users_data[user_id]['msg_list'][chat_id][msg_id] = {}
			users_data[user_id]['msg_list'][chat_id][msg_id]['text'] = text
			users_data[user_id]['msg_list'][chat_id][msg_id]['send_uid'] = user_id
			users_data[user_id]['msg_list'][chat_id][msg_id]['timestamp'] = timestamp

		else:
			users_data[user_id]['msg_list'][chat_id] = {}
			users_data[user_id]['msg_list'][chat_id][msg_id] = {}
			users_data[user_id]['msg_list'][chat_id][msg_id]['text'] = text
			users_data[user_id]['msg_list'][chat_id][msg_id]['send_uid'] = user_id
			users_data[user_id]['msg_list'][chat_id][msg_idmsg_id]['timestamp'] = timestamp

	return redirect('/dashboard/'+str(user_id))


@app.route("/fetch_msgs/<string:user_id>", methods = ['GET', 'POST'])
def fetch_msgs(user_id):
	global users_data, producer
	chat_id = users_data[user_id]["cid"]
	if chat_id != None:
		chat_id = chat_id.strip()

	dict_msg = {
		"op_type":"fetch_msgs",
		"uid1" : user_id,
		"uid2" : chat_id
	}

	topic = "ActionServer"
	producer.send(topic, json.dumps(dict_msg).encode('utf-8'))

	return redirect('/dashboard/'+str(user_id))


@app.route("/update_msg/<string:user_id>", methods=['GET', 'POST'])
def update_msg(user_id):
	global users_data, msg_count, producer
	if (request.method == 'POST'):
		req = request.form
		req = dict(req)
		print(req)
		text = str(req['text'])
		msg_id = str(req['msg_id'])
		chat_id = users_data[user_id]['cid']
		timestamp = str(datetime.datetime.now())
		if chat_id != None:
			chat_id = chat_id.strip() 
		
		dict_msg = {
			"op_type":"update_msg",
			"uid1":user_id,
			"uid2":chat_id,
			"text":text,
			"msg_id":msg_id,
			"timestamp": timestamp
		}

		topic = "ActionServer"
		producer.send(topic, json.dumps(dict_msg).encode('utf-8'))

		if chat_id in users_data[user_id]['msg_list']:
			users_data[user_id]['msg_list'][chat_id][msg_id]['text'] = text
			users_data[user_id]['msg_list'][chat_id][msg_id]['timestamp'] = timestamp
			
	return redirect('/dashboard/'+str(user_id))


@app.route("/delete_msg/<string:user_id>", methods=['GET', 'POST'])
def delete_msg(user_id):
	global users_data, msg_count, producer
	if (request.method == 'POST'):
		req = request.form
		req = dict(req)
		print(req)
		msg_id = str(req['msg_id'])
		chat_id = users_data[user_id]['cid']
		if chat_id != None:
			chat_id = chat_id.strip() 
		
		dict_msg = {
			"op_type":"delete_msg",
			"uid1":user_id,
			"uid2":chat_id,
			"msg_id":msg_id
		}

		topic = "ActionServer"
		producer.send(topic, json.dumps(dict_msg).encode('utf-8'))

		if chat_id in users_data[user_id]['msg_list']:
			users_data[user_id]['msg_list'][chat_id].pop(msg_id)
			
					
	return redirect('/dashboard/'+str(user_id))


@app.route("/logout/<string:user_id>", methods=['GET', 'POST'])
def logout(user_id):
	global users_data
	print("logout ", user_id)
	users_data.pop(user_id)
	return redirect('/home')


# ip: localhost (127.0.0.1) and port 5000
if __name__ == "__main__":
    app.run(debug=True, threaded=True)