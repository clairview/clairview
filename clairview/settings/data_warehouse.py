import os

AIRBYTE_API_KEY = os.getenv("AIRBYTE_API_KEY", None)
AIRBYTE_BUCKET_REGION = os.getenv("AIRBYTE_BUCKET_REGION", None)
AIRBYTE_BUCKET_KEY = os.getenv("AIRBYTE_BUCKET_KEY", None)
AIRBYTE_BUCKET_SECRET = os.getenv("AIRBYTE_BUCKET_SECRET", None)
AIRBYTE_BUCKET_DOMAIN = os.getenv("AIRBYTE_BUCKET_DOMAIN", None)
# for DLT
BUCKET_URL = os.getenv("BUCKET_URL", None)
AIRBYTE_BUCKET_NAME = os.getenv("AIRBYTE_BUCKET_NAME", None)
BUCKET = "test-pipeline"