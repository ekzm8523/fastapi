import os
from base64 import b64encode
from datetime import timedelta

DB_INFO = {
    'USER': os.getenv('AI_DB_USER'),
    'NAME': os.getenv('AI_DB_NAME'),
    'PASSWORD': os.getenv('AI_DB_PASSWORD'),
    'HOST': os.getenv('AI_DB_HOST'),
    'PORT': os.getenv('AI_DB_PORT')
}

DATABASE_URL = f"postgresql://{DB_INFO['USER']}" \
               f":{DB_INFO['PASSWORD']}" \
               f"@{DB_INFO['HOST']}" \
               f":{DB_INFO['PORT']}" \
               f"/{DB_INFO['NAME']}"


JWT_SECRET_KEY = os.getenv('AI_TOOLS_SECRET_KEY', '')

JWT_AUTH = {
    'JWT_SECRET_KEY': b64encode(JWT_SECRET_KEY.encode()).decode(),
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(hours=24),  # timedelta(minutes=1),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': 'Jack',
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),  # timedelta(minutes=1),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}


# develop: dev, stage: stg
DEVELOP_MODE = 'ai-tools-dev'


