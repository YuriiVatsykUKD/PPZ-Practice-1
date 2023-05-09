from typing import Optional, Union
import boto3
from botocore.exceptions import ClientError
import pyodbc


DATABASE_VALUE = 'TestDB' 
ENVIRONMENT = 'stg'
RDS_INSTANCE_VALUE = f"test_api-{ENVIRONMENT}"
REGION_VALUE = "apse2"
AWS_REGION = "ap-southeast-2"
S3_BUCKET_NAME_ARN = 'arn:aws:s3:::test-rds-backup-to-s3-lambda'
S3_OBJECT_KEY = f"{ENVIRONMENT}/{RDS_INSTANCE_VALUE}"
FILE_NAME = f"{DATABASE_VALUE}-{RDS_INSTANCE_VALUE}-{REGION_VALUE}"
HOST_VALUE = f"/rds/{RDS_INSTANCE_VALUE}/endpoint"
USER_VALUE = f"/rds/{RDS_INSTANCE_VALUE}/user"
PASSWORD_VALUE = f"/rds/{RDS_INSTANCE_VALUE}/password"
SQL_SELECT = f"""exec msdb.dbo.rds_backup_database
                 @source_db_name='{DATABASE_VALUE}',
                 @s3_arn_to_backup_to='{S3_BUCKET_NAME_ARN}/{S3_OBJECT_KEY}/{FILE_NAME}.bak',
                 @overwrite_s3_backup_file=1,
                 @number_of_files=1;"""

ssm_client = boto3.client("ssm", region_name=AWS_REGION)


def get_parameter(name1: str) -> Optional[Union[str, bytes]]:

    try:
        parameter_value = ssm_client.get_parameter(Name=name1, WithDecryption=True)
        return parameter_value['Parameter']['Value']
    except ClientError as error:
        print(f"An error occurred: {error}", err=True)
    return None

def lambda_handler(event, context):

    host = get_parameter(HOST_VALUE)
    user = get_parameter(USER_VALUE)
    password = get_parameter(PASSWORD_VALUE)

    connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                            f"""SERVER={host};
                            DATABASE={DATABASE_VALUE};
                            UID={user};
                            PWD={password}""")

    cursor = connection.cursor()
    cursor.execute(SQL_SELECT)
    cursor.close()
    connection.commit()
    connection.close()

    print("Process finished")

    return {
        'statusCode': 200
    }