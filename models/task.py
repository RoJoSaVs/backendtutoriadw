import datetime
import json


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
