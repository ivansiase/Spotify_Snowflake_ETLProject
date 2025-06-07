CREATE STORAGE INTEGRATION my_s3_integration
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = S3
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::881414777122:role/s3-snowflake-connection'
    STORAGE_ALLOWED_LOCATIONS = ('s3://siase-spotify-pipeline')

    desc integration my_s3_integration