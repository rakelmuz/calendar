# -- coding: utf-8 --
#Usado para retornar os dados processados ​​no formato json
import json
#python mysql Driver de conexão
import pymysql

#db função de conexão
def getConnection():
    return pymysql.connect(host='localhost', user='root', password='123456789',
                           db='calendar', charset='utf8')

#Mudança de formato para que o valor do formato mysql datetime entre os dados selecionados possa ser processado em fullCalendar
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def sql_template(type, sql, params=None):
    # Connection 
    connetion = getConnection()
    try:
        #insert, update, delete 
        if type == 3 :
            with connetion.cursor() as cursor :
                # Entrada de dados
                rows = cursor.execute(sql, params)
                # commit
                connetion.commit()
                return rows
        else :
            # 1 = fetchall() 2 = fetchone()
            with connetion.cursor(pymysql.cursors.DictCursor) as cursor :
                cursor.execute(sql, params)
                if type == 1 :
                    return cursor.fetchall()
                elif type == 2 :
                    return cursor.fetchone()
    finally:
        # finaliza conexão
        connetion.close()

#obter os eventos cadastrados
def getEvento(searchDate):
    if not parameter_checker(searchDate) :
        return json.dumps({})
    sql = "select id, title, start, end from evento where to_days(start) >= to_days(%s) and to_days(end) <= to_days(%s)"
    params = ( searchDate['start'], searchDate['end'])
    #Altera os dados  ​​para json, date_handler para processamento de data e hora
    return json.dumps(sql_template(1, sql, params), default=date_handler);

#inserir evento
def setEvento(schedule):
    #Retorna 0 se houver um valor vazio nos dados passados
    if not parameter_checker(schedule) :
        return json.dumps({'rows' : 0})
    else :
        sql = "INSERT INTO evento(title, start, end) VALUES (%s, %s, %s)"
        params = (schedule['title'], schedule['start'], schedule['end'])
        return json.dumps({'rows' : sql_template(3, sql, params)})

# deletar evento
def delEvento(id):
    #Retorna 0 se houver um valor vazio nos dados passados
    if not parameter_checker(id) :
        return json.dumps({'rows' : 0})
    else :
        sql = "DELETE FROM evento WHERE id = %s"
        params = (id)
        return json.dumps({'rows' : sql_template(3, sql, params)})

#Editar evento
def putEvento(schedule):
    #Retorna 0 se houver um valor vazio nos dados passados
    if not parameter_checker(schedule) :
        return json.dumps({'rows' : 0})
    else :
        sql = "UPDATE evento SET title = %s, start = %s, end = %s WHERE id = %s"
        params = (schedule['title'], schedule['start'], schedule['end'], schedule['id'])
        return json.dumps({'rows' : sql_template(3, sql, params)})

# verificar parametro em branco
def parameter_checker(params):
    
    if not bool(params):
        return False
    #No caso de str ou unicode, verifique se a string aparada está em branco
    elif hasattr(params,'strip') and not bool(params.strip()):
            return False
    
    elif hasattr(params,'values'):
        for value in params.values() :
            if not parameter_checker(value) :
                return False
        return True
    else:
        return True
