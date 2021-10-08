import os

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

# develop: dev, stage: stg
DEVELOP_MODE = 'dev'


