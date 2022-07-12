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

