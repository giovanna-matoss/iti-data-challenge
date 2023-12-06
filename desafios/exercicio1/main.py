import boto3
from moto import mock_sqs

import event_validator as event_validator

@mock_sqs
def main(event):
    _SQS_CLIENT = boto3.client('sqs', region_name='us-east-1')
    _SQS_CLIENT.create_queue(
        QueueName='valid-events-queue'
    )
    event_validator._SQS_CLIENT = _SQS_CLIENT
    event_validator.handler(event)
    
if __name__ == "__main__":
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }

    # Testes para validar campos de entrada
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "middle_name": "Andre",
        "last_name": "Smith",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "middle_name": "Joseph",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "first_name": "Joseph",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "age": 32,
        "address": {
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "age": 32,
        "address": {
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "age": 32,
        "address": {
            "mailAddress": True
        },
        "name": "Joseph",
        "test": {
            "string": "Only a test"
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "mailAddress": True
        }
    }
    """


    # Testes para validar tipos dos dados
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "age": "32",
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": 42323235600,
        "name": "Joseph",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": 42323235600,
        "name": "Joseph",
        "age": "32",
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": "3",
            "mailAddress": True
        }
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "address": {
            "street": "St. Blue",
            "number": "3",
            "mailAddress": True
        },
        "name": "Joseph",
        "age": "32"
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "test": {
            "string": "Only a test",
            "integer": 5,
            "boolean": True
        },
        "documentNumber": "42323235600",
        "address": {
            "street": "St. Blue",
            "number": "3",
            "mailAddress": True
        },
        "name": "Joseph",
        "age": "32"
    }
    """
    """
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "test": {
            "string": "Only a test",
            "integer": "5",
            "boolean": 0
        },
        "documentNumber": "42323235600",
        "address": {
            "street": "St. Blue",
            "number": "3",
            "mailAddress": True
        },
        "name": "Joseph",
        "age": "32"
    }
    """


    main(event)