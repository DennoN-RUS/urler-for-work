# coding: utf-8
import os
import logging
import src.cross_auth as cauth
import src.git as git

if os.environ.get("debug", 'false') == "true":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-4s %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-4s %(message)s')

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

method = os.environ.get('method', None)
env = os.environ.get('env', None)
serviceName = os.environ.get('serviceName', None)
login = os.environ.get('login', None)
password = os.environ.get('password', None)
values = os.environ.get('values', None)

tokenLifetime = os.environ.get('tokenLifetime', None)

envs = ["dev","rc","prod"]
mass = dict()

# Проверка, что бы не задать один пароль на все окружения
if env == "all":
    password = ''
# Перебор всех окружений
for cur_env in envs:
    if env == "all" or env == cur_env:
        # Деграем cross-auth-backend по нужной ручке в нужном окружении
        if method == "client_add":
            password = cauth.add(cur_env,login,password,serviceName,values,tokenLifetime)
        elif method == "client_update":
            cauth.update(cur_env,login,serviceName,values,tokenLifetime)
        elif method == "client_change-password":
            password = cauth.change_pass(cur_env,login,password)
        # Сохраняем пароль в словарь
        if method =="client_add" or method == "client_change-password":
            if mass == {}:
                mass = git.get_dict() # Получаем текущий список
            mass = git.add_to_dict(cur_env,login,password,mass) # Добавляем пароль в словарь
        cauth.get_info(cur_env,login) # Выводим инфу о сервисe
# Отправляем пароли в гит
if mass != {}:
    git.send_dict(mass,env,login)





