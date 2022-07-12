import json
# data = ["DisneyPlus", "Netflix", "Peacock"]
# json_string = json.dumps(data)
# print(json_string)


def listFormatResponse(listOfList):
	listFormat = []
	for elemList in listOfList:
		jsonFormat = '{"_id":%s, "nombre":"%s"}' %(elemList[0], elemList[1])
		listFormat.append(json.loads(jsonFormat))
	return json.dumps(listFormat)



def formatValuesToInsertList(listToInsert):
	_id = listToInsert['_id']
	nombre = listToInsert['nombre']
	