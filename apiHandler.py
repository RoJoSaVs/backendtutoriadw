import flask
from flask import request, jsonify, g, render_template, abort
from flask_cors import CORS, cross_origin
import json
import sys
import postgresqlHandler
from models.task import *
from models.list import *

app = flask.Flask(__name__)
CORS(app, support_credentials=True)
# handler = postgresqlHandler.PostgresqlHandler("localhost", "postgres", "postgres", "2659")
handler = postgresqlHandler.PostgresqlHandler("ec2-44-206-89-185.compute-1.amazonaws.com", "d1m7093pnmaqa2", "vtqffnrzjvinle", "fd1a1c35d91f5eb3f87c4bb65073e5442ab5c839ad2fc0a2b8ec7d45b5566d62")


# Lists methods
@app.route('/get/list/<param>', methods=['GET'])
def getList(param):
	response = listFormatResponse(handler.getListForUser(param))
	return response
    # print(param, file=sys.stderr)


@app.route('/add/list/<param>', methods=['POST'])
def addList(param):
	data = request.json
	handler.addList(data['nombre'], param)
	return "0"


@app.route('/edit/list/<param>', methods=['PUT'])
def editList(param):
	_id = request.args.get('_id')
	data = request.json
	handler.editList(data['nombre'], _id)
	return "0"


@app.route('/delete/list/<param>', methods=['DELETE'])
def deleteList(param):
	_id = request.args.get('_id')
	handler.deleteList(_id)
	return "0"	





# Task
@app.route('/get/task/<param>', methods=['GET'])
def getTask(param):
    # print(param, file=sys.stderr)
    response = formatResponse(handler.getTaskForUser(param))
    return response



@app.route('/add/task/<param>', methods=['POST'])
def addTask(param):
	data = request.json
	handler.addTaskToList(formatValuesToInsert(data))
	return "0"



@app.route('/edit/task/<param>', methods=['PUT'])
def editTask(param):
	_id = request.args.get('_id')
	data = request.json
	handler.editTask(formatValuesToEdit(data), _id)
	return "0"



@app.route('/delete/task/<param>', methods=['DELETE'])
def deleteTask(param):
	_id = request.args.get('_id')
	handler.deleteTask(_id)
	return "0"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# app.run()