import subprocess
import sys
import datetime
import json

import flask
from flask import request, jsonify, g, render_template, abort
from flask_cors import CORS, cross_origin



# Help to install packages form python file (this was made to works with replit)
# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Install every package needed
# Package name should be used

# install("psycopg2")
# install("dnspython")
# install("Flask")
# install("Flask-Cors")


####################################################################
########################### POSTGRESQL #############################
####################################################################
import psycopg2

class PostgresqlHandler:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        self.cursor = self.connection.cursor()



    # Get all lists related to a user
    def getListForUser(self, userToken):
        try:
            self.cursor.execute("""SELECT Lista._id, Lista.nombre FROM Lista 
                                    INNER JOIN  Cuenta ON lista.listaUsuario = cuenta.tokenUsuario 
                                    WHERE cuenta.tokenUsuario = '%s';""" %(userToken))
            result = self.cursor.fetchall()
            return result

        except:
            return []


    # Add a new List to database
    # def addList(self, listToAdd):
    def addList(self, listToAddName, listToAddUserToken):
        try:
            insertQuery = "INSERT INTO Lista (nombre, listaUsuario) VALUES ('%s', '%s')" %(listToAddName, listToAddUserToken)
            self.cursor.execute(insertQuery)
            self.connection.commit()
            return True

        except:
            return False


    # Edit a List attribute based on it's id
    def editList(self, nameList, listId):
        try:
            editListQuery = "UPDATE Lista SET nombre = '%s' WHERE _id = '%s'" %(nameList, listId)
            self.cursor.execute(editListQuery)
            self.connection.commit()
            return True
        except:
            return False


    # Delete a List by id always that this doesn't have a Task related
    def deleteList(self, listId):
        try:
            deleteListQuery = "DELETE FROM Lista WHERE _id = %s" %(listId)
            self.cursor.execute(deleteListQuery)
            self.connection.commit()
            return True

        except:
            return False




    # Get all tasks related to a list
    def getTaskForList(self, listId):
        try:
            self.cursor.execute("""SELECT  Tarea._id, Tarea.nombre, Tarea.descripcion, Tarea.urgenciaString, 
                                Tarea.urgenciaNumber, Tarea.fechaVencimiento, Tarea.estado, Tarea.posicion, 
                                Tarea.datosContacto, Tarea.categoriaLista, Lista.nombre FROM
                                Tarea INNER JOIN Lista ON Lista._id = Tarea.categoriaLista
                                WHERE Lista._id = %s;""" %(listId))
            result = self.cursor.fetchall()
            return result

        except:
            return []



    # Get all tasks related to a user
    def getTaskForUser(self, userToken):
        try:
            self.cursor.execute("""SELECT Tarea._id, Tarea.nombre, Tarea.descripcion, Tarea.urgenciaString, 
                                Tarea.urgenciaNumber, Tarea.fechaVencimiento, Tarea.estado, Tarea.posicion, 
                                Tarea.datosContacto, Tarea.categoriaLista, Lista.nombre FROM 
                                (
                                    (
                                        Tarea INNER JOIN Lista ON Lista._id = Tarea.categoriaLista
                                    ) 
                                    INNER JOIN Cuenta ON lista.listaUsuario = cuenta.tokenUsuario
                                ) 
                                WHERE cuenta.tokenUsuario = '%s';""" %(userToken))
            result = self.cursor.fetchall()
            return result

        except:
            return []


    # Add a new Task to a list
    def addTaskToList(self, taskToAdd):
        try:
            insertQuery = "INSERT INTO Tarea (nombre, descripcion, urgenciaString, urgenciaNumber, fechaVencimiento, estado, posicion, datosContacto, categoriaLista) VALUES %s"%(taskToAdd)
            self.cursor.execute(insertQuery)
            self.connection.commit()
            print(taskToAdd)
            return True

        except:
            return False


    # Edit a Task attributte based on it's id
    def editTask(self, updateString, taskId):
        try:
            editTaskQuery = "UPDATE Tarea SET %s WHERE _id = %s;"%(updateString, taskId)
            self.cursor.execute(editTaskQuery)
            self.connection.commit()
            return True
            
        except:
            return False


    # Delete a Task by id
    def deleteTask(self, taskId):
        try:
            deleteTaskQuery = "DELETE FROM Tarea WHERE _id = %s" %(taskId)
            self.cursor.execute(deleteTaskQuery)
            self.connection.commit()
            return True

        except:
            return False


####################################################################
######################## LISTA #####################################
####################################################################


def listFormatResponse(listOfList):
    listFormat = []
    for elemList in listOfList:
        jsonFormat = '{"_id":%s, "nombre":"%s"}' %(elemList[0], elemList[1])
        listFormat.append(json.loads(jsonFormat))
    return json.dumps(listFormat)



def formatValuesToInsertList(listToInsert):
    _id = listToInsert['_id']
    nombre = listToInsert['nombre']


####################################################################
######################## TAREA #####################################
####################################################################
def formatResponse(taskList):
    taskListFormat = []
    for task in taskList:
        jsonFormat = '{"_id":%s, "nombre":"%s", "descripcion":"%s", "urgenciaString":"%s", "urgenciaNumber":%s, "fechaVencimiento":"%s", "estado":"%s", "posicion":%s, "datosContacto":"%s", "Lista":{"categoriaLista":"%s", "nombreLista":"%s"}}' %(task[0], task[1], task[2], task[3], task[4], str(task[5]), task[6], task[7], task[8], task[9], task[10])
        taskListFormat.append(json.loads(jsonFormat))
    return json.dumps(taskListFormat)


# ('main', 'descripcion', 'Urgente', 5, '2022-07-22', 'Pendiente', 0, 'datos de contacto', 11)
def formatValuesToInsert(taskToInsert):
    # _id = taskToInsert['_id']
    nombre = taskToInsert['nombre']
    descripcion = taskToInsert['descripcion']
    urgenciaString = taskToInsert['urgenciaString']
    urgenciaNumber = taskToInsert['urgenciaNumber']
    fechaVencimiento = taskToInsert['fechaVencimiento']
    estado = taskToInsert['estado']
    posicion = taskToInsert['posicion']
    datosContacto = taskToInsert['datosContacto']
    categoriaLista = taskToInsert['Lista']['categoriaLista']
    # taskString = """('%s', '%s', '%s', %s, '%s', '%s', %s, '%s', '%s')""" %(nombre, descripcion, urgenciaString, urgenciaNumber, fechaVencimiento, estado, posicion, datosContacto, categoriaLista)
    taskString = """('%s', '%s', '%s', %s, '%s', '%s', %s, '%s', %s)""" %(nombre, descripcion, urgenciaString, urgenciaNumber, fechaVencimiento, estado, posicion, datosContacto, categoriaLista)
    return taskString


def formatValuesToEdit(taskToUpdate):
    nombre = taskToUpdate['nombre']
    descripcion = taskToUpdate['descripcion']
    urgenciaString = taskToUpdate['urgenciaString']
    urgenciaNumber = taskToUpdate['urgenciaNumber']
    fechaVencimiento = taskToUpdate['fechaVencimiento']
    estado = taskToUpdate['estado']
    posicion = taskToUpdate['posicion']
    datosContacto = taskToUpdate['datosContacto']
    categoriaLista = taskToUpdate['Lista']['categoriaLista']
    # taskString = "(nombre='%s', descripcion='%s', urgenciaString='%s', urgenciaNumber=%s, fechaVencimiento='%s', estado='%s', posicion=%s, datosContacto='%s', categoriaLista='%s')"%(nombre, descripcion, urgenciaString, urgenciaNumber, fechaVencimiento, estado, posicion, datosContacto, categoriaLista)
    taskString = "nombre='%s', descripcion='%s', urgenciaString='%s', urgenciaNumber=%s, fechaVencimiento='%s', estado='%s', posicion=%s, datosContacto='%s', categoriaLista=%s"%(nombre, descripcion, urgenciaString, urgenciaNumber, fechaVencimiento, estado, posicion, datosContacto, categoriaLista)
    return taskString


####################################################################
####################### API HANDLER ################################
####################################################################
app = flask.Flask(__name__)
CORS(app, support_credentials=True)
# handler = postgresqlHandler.PostgresqlHandler("localhost", "postgres", "postgres", "2659")
handler = PostgresqlHandler("ec2-44-206-89-185.compute-1.amazonaws.com", "d1m7093pnmaqa2", "vtqffnrzjvinle", "fd1a1c35d91f5eb3f87c4bb65073e5442ab5c839ad2fc0a2b8ec7d45b5566d62")


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


####################################################################
########################### MAIN ###################################
####################################################################
# import apiHandler
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # apiHandler.app.run(host='0.0.0.0', port=5000, debug=True)