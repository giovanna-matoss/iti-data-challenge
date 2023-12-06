import boto3
from moto import mock_athena, mock_s3

import json_schema_to_hive as js_2_hive

@mock_athena
@mock_s3
def main():
    _S3_CLIENT = boto3.client("s3", region_name='us-east-1')
    _S3_CLIENT.create_bucket(Bucket='iti-query-results')

    _ATHENA_CLIENT = boto3.client('athena', region_name='us-east-1')

    js_2_hive._ATHENA_CLIENT = _ATHENA_CLIENT
    js_2_hive.handler()
    
if __name__ == "__main__":
    main()