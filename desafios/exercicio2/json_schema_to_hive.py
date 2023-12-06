import json
_ATHENA_CLIENT = None

def create_hive_table_with_athena(query):
    '''
    Função necessária para criação da tabela HIVE na AWS
    :param query: Script SQL de Create Table (str)
    :return: None
    '''
    
    print(f"Query: {query}")
    _ATHENA_CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': f's3://iti-query-results/'
        }
    )

def handler():
    '''
    #  Função principal
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função create_hive_table_with_athena para te auxiliar
        na criação da tabela HIVE, não é necessário alterá-la
    '''

    # Realizando leitura do schema validador
    file = open('desafios\exercicio2\schema.json')
    validator_schema = json.load(file)

    query = generate_query(validator_schema, 'event', 's3://bucket/folder/', 'challenge')
    create_hive_table_with_athena(query)

# Função responsável por preparar e normalizar os campos que serão utlizados para criar a tabela
def generate_formatted_fields(schema, object_schema=[], line=0):
    formatted_fields = []
    schema = object_schema if object_schema else schema
    separator = " " if line==0 else ': '
    end_line = ',\n'
    new_line = line + 1
    indentation = new_line * "  "
    
    for field_name, attr in schema.items():
        if attr['type']=='object':
            formatted_fields.append("{indentation}{field_name}{separator}STRUCT<\n{fields}\n{indentation}>"
                .format(
                    indentation=indentation,
                    field_name=field_name,
                    separator=separator,
                    fields=generate_formatted_fields(schema, attr['properties'], new_line)
                )
            )

        else:
            field_type = attr['type'].upper()
            formatted_fields.append(f"{indentation}{field_name}{separator}{field_type}")
    
    return end_line.join(formatted_fields)


# Função responsável por gerar a query de criação de tabela
def generate_query(schema, table_name, location='', database=''):
    formatted_fields = generate_formatted_fields(schema['properties'])
    location = f"LOCATION '{location}'"

    query = f"""
CREATE EXTERNAL TABLE {database}.{table_name} ( 
{formatted_fields} 
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
{location}"""

    return query