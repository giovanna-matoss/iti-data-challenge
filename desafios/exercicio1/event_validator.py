import json
import boto3

_SQS_CLIENT = None

def send_event_to_queue(event, queue_name):
    '''
     Responsável pelo envio do evento para uma fila
    :param event: Evento  (dict)
    :param queue_name: Nome da fila (str)
    :return: None
    '''
    
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.get_queue_url(
        QueueName=queue_name
    )
    queue_url = response['QueueUrl']
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(event)
    )
    print(f"Response status code: [{response['ResponseMetadata']['HTTPStatusCode']}]")

def handler(event):
    '''
    #  Função principal que é sensibilizada para cada evento
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função send_event_to_queue para envio do evento para a fila,
        não é necessário alterá-la
    '''

    # Realizando leitura do schema validador
    file = open('desafios\exercicio1\schema.json')
    validator_schema = json.load(file)

    # Aplicando validações
    must_contain(event, validator_schema)
    validate_data_type(event, validator_schema)

    send_event_to_queue(event, 'valid-events-queue')


# Função responsável por validar campos obrigatórios
def must_contain(event, schema):
    required_fields = schema['required']
    entry_fields = list(event)
    mismatching_fields = []
    
    # Somente realiza comparação entre schemas, sem informar divergências
    if set(entry_fields) != set(required_fields):
        raise Exception("Event schema doesn't match with required schema!")

    # Comparação do tamanho dos schemas
    # Algum campo não necessário sendo enviado
    if len(entry_fields) > len(required_fields):
        for e_field in entry_fields:
            if e_field not in required_fields:
                mismatching_fields.append(e_field)
        if mismatching_fields:
            raise Exception(f"Different schema sizes! Event field: {mismatching_fields} is not required.")
        
    # Comparação do tamanho dos schemas
    # Faltando algum campo requerido
    if len(entry_fields) < len(required_fields):
        for r_field in required_fields:
            if r_field not in entry_fields:
                mismatching_fields.append(r_field)
    
    # Validação para campos que possuem sub-campos como requeridos
    for e_field in entry_fields:
        if schema['properties'][e_field]['type']=='object':
            object_fields = list(event[e_field])
            required_fields = schema['properties'][e_field]['required']
            if len(object_fields) < len(required_fields):
                for r_field in required_fields:
                    if r_field not in object_fields:
                        mismatching_fields.append(r_field)

    if mismatching_fields:
        raise Exception(f"Different schema sizes! Event field: {mismatching_fields} is missing.")


# Função responsável por validar tipos de dados
def validate_data_type(event, schema, mismatching_fields={}, object_fields=[], object_event={}, object_schema=[]):
    required_schema = object_schema['properties'] if object_schema else schema['properties']
    entry_data = object_event.items() if object_event else event.items()

    for entry_field, entry_value in entry_data:
        # Validação para campos que possuem sub-campos
        if required_schema[entry_field]['type']=='object':
            object_fields.append(entry_field)

        else:
            entry_type = type(entry_value)
            required_type = type(required_schema[entry_field]['examples'][0])

            if entry_type != required_type:
                if not mismatching_fields:
                    mismatching_fields = {
                        entry_field: {
                            'entry_type': entry_type,
                            'required_type': required_type
                        }
                    }
                else:
                    mismatching_fields.update({
                            entry_field: {
                                'entry_type': entry_type,
                                'required_type': required_type
                            } 
                        }
                    )
    
    # Validação para campos que possuem sub-campos
    if object_fields:
        for o_field in object_fields:
            object_fields.remove(o_field)
            validate_data_type(event, schema, mismatching_fields, object_fields, object_event=event[o_field], object_schema=schema['properties'][o_field])

    if mismatching_fields:
        raise Exception(f"Data type error! See more about the error here: {mismatching_fields}")
