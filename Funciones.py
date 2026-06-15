import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('t_alumnos')

def crear(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    alumno_datos = event['body']['alumno_datos']
    # Proceso
    alumno = {
        'tenant_id': tenant_id,
        'alumno_id': alumno_id,
        'alumno_datos': alumno_datos
    }
    response = table.put_item(Item=alumno)
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }

def listar(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    # Proceso
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    items = response['Items']
    num_reg = response['Count']
    print(items)
    # Salida (json)
    return {
        'statusCode': 200,
        'tenant_id': tenant_id,
        'num_reg': num_reg,
        'alumnos': items
    }

def modificar(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    alumno_datos = event['body']['alumno_datos']
    # Proceso
    response = table.update_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id},
        UpdateExpression='SET alumno_datos = :datos',
        ExpressionAttributeValues={':datos': alumno_datos},
        ReturnValues='ALL_NEW'
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'alumno': response['Attributes']
    }

def eliminar(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # Proceso
    response = table.delete_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id}
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'mensaje': 'Alumno eliminado',
        'tenant_id': tenant_id,
        'alumno_id': alumno_id
    }

def buscar(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # Proceso
    response = table.get_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id}
    )
    # Salida (json)
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'mensaje': 'Alumno no encontrado'
        }
    return {
        'statusCode': 200,
        'alumno': response['Item']
    }
