# CSC4001
For our Team Project
<<<<<<< Updated upstream
=======


## environment
### copy and paste to some txt, and run pip install -r xxx.txt
asgiref            ==3.5.0
boto3              ==1.21.42
botocore           ==1.24.42
certifi            ==2021.10.8
cffi               ==1.15.0
charset-normalizer ==2.0.12
cryptography       ==36.0.2
Django             ==4.0.4
django-storages    ==1.12.3
gunicorn           ==20.1.0
idna               ==3.3
jmespath           ==1.0.0
Naked              ==0.1.31
Pillow             ==9.1.0
pip                ==22.0.4
psycopg2           ==2.9.3
pycparser          ==2.21
pycryptodomex      ==3.9.4
PyMySQL            ==1.0.2
pyOpenSSL          ==19.1.0
python-alipay-sdk  ==3.0.4
python-dateutil    ==2.8.2
pytz               ==2022.1
PyYAML             ==6.0
requests           ==2.27.1
s3transfer         ==0.5.2
setuptools         ==58.1.0
shellescape        ==3.8.1
six                ==1.16.0
sqlparse           ==0.4.2
tzdata             ==2022.1
urllib3            ==1.26.9
whitenoise         ==6.0.0

## runing commands
### make sure the cmd is in the root dir of the PJ 
$ pip -r install xxx.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

## already exists some users in the DB
username            password
jim3                jim3_pwd_123
jim4                jim4_pwd_123
MySU                MySU_pwd_123

## what we didn't provide:
### 1. qq mail for validation email sneding
### 2. remote database conf
### 3. remote server conf
we did not provide these due to the consideration of privacy, 
we will demo it on the presentation

## what we haven't really achieve due to some 审核:
### alipay API
It can be used in the test-version alipay, instead of the real one
>>>>>>> Stashed changes
