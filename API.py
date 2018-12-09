from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'somedb'
app.config['MONGO_URI'] = 'mongodb://zeelee28:abc123@ds027165.mlab.com:27165/somedb'
mongo = PyMongo(app)

# GET all users in collection
@app.route('/')
# def hello():
#     return 'hello world!'
def get_all_users():
    users = mongo.db.users
    output = []
    for q in users.find():
        output.append({'first_name' : q['first_name'], 'last_name' : q['last_name']})
    return jsonify({'result': output})

# GET users by first name
@app.route('/<string:first_name>', methods=['GET'])
def get_one_user(first_name):
    users = mongo.db.users
    q = users.find_one({'first_name': first_name})
    if q:
        output = {'first_name': q['first_name'], 'last_name' : q['last_name']}
    else:
        output = 'No results found'
    return jsonify({'result' : output})

# ADD new users
@app.route('/', methods=['POST'])
def add_user():
    users = mongo.db.users

    first_name = request.json['first_name']
    last_name = request.json['last_name']

    user_id = users.insert({'first_name' : first_name,'last_name' : last_name})
    new_user = users.find_one({'_id' : user_id})

    output = {'first_name' : new_user['first_name'], 'last_name' : new_user['last_name']}

    return jsonify({'result' : output})

# Update user info
@app.route('/<string:fname>', methods=['PUT'])
def update_user(fname):
    users = mongo.db.users

    first_name = request.json['first_name']
    last_name = request.json['last_name']

    q = users.find_one_and_update({'first_name': fname},{'$set':{'first_name': first_name,'last_name':last_name}})
    if q:
        output = {'first_name': first_name,'last_name':last_name}
    else:
        output = 'Sorry. User does not exist.'
    return jsonify({'result' : output})

# Delete user info
@app.route('/<string:first_name>', methods=['DELETE'])
def delete_user(first_name):
    users = mongo.db.users
    q = users.delete_one({'first_name': first_name})
    if q:
        # output = 'you deleted something'
        output = {'You deleted' : first_name}
    else:
        output = 'Cannot delete user that does not exist.'
    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)