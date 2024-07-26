# coding: utf-8
import os
import requests
import json
import logging
import random
import string
import src.utlis as util

__url_dev="dev_url"
__url_rc="rc_url"
__url_prod="prod_url"
__path_add="path_add"
__path_update="path_update"
__path_change_pass="path_change_pass"
__path_get_info="path_get_info"

# Генерация паролья заданной длины
def __gen_pass(length):
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Проверка переменной, а так же если пароль пустой, то создание пароля
def __check_variable(name,value):
    if name == "password":
        if value is None or value.strip() == '':
            value = __gen_pass(20)
    elif value is None or value.strip() == '':
        exit("\nVariable " + name + " not defined!\n")
    return value

# Получение url сервиса в заивисмости от окружения
def __get_url(env):
    if env == "prod":
        return __url_prod
    elif env == "rc":
        return __url_rc
    elif env == "dev":
        return __url_dev

# Получение xPassKeys и генериация хиредов
def __get_headers(env):
    if env == "prod":
        xPassKeys =  os.environ['xPassKeys_prod']
    else:
        xPassKeys = os.environ['xPassKeys_devrc']
    headers = {"Content-Type": "application/json-patch+json", "X-Pass-Key": xPassKeys }
    return headers

# Генерация части тела запроса (permissions)
def __gen_permissions(serviceName,values):
    serv = serviceName.split("|")
    val = values.split("|")
    if len(serv) != len(val):
        exit("\nserviceName and values dont match\n")
    permissions = []
    for i in range(len(serv)):
        permissions += [{"serviceName": serv[i], "values": val[i].split()}]
    return permissions

# Вывести текущие доступы по логину и окружению
def get_info(env,login):
    p = {"login": login}
    url = __get_url(env)
    headers = __get_headers(env)
    r = requests.get(url + "/" + __path_get_info, headers=headers, params=p)
    util.check_request(r)
    logging.info("")
    logging.info(env)
    logging.info(r.text)
    logging.info("")

# Добавить новый логин в окружение с заданными параметрами
def add(env,login,password,serviceName,values,tokenLifetime):
    __check_variable("values", values)
    __check_variable("serviceName", serviceName)
    __check_variable("tokenLifetime", tokenLifetime)

    password = __check_variable("password", password)
    url = __get_url(env)
    headers = __get_headers(env)
    permissions = __gen_permissions(serviceName,values)
    data = json.dumps( 
            {"login": login,
            "password": password,
            "permissions": permissions,
            "tokenLifetime": tokenLifetime}
    )
    logging.debug("data: {}".format(data))
    util.check_request( requests.post(url + "/" + __path_add, headers=headers, data=data) )
    return password

# Обновить параметры у указанного логина в нужном окружении
def update(env,login,serviceName,values,tokenLifetime):
    __check_variable("values", values)
    __check_variable("serviceName", serviceName)
    __check_variable("tokenLifetime", tokenLifetime)

    url = __get_url(env)
    headers = __get_headers(env)
    permissions = __gen_permissions(serviceName,values)
    data = json.dumps( 
            {"login": login,
            "permissions": permissions,
            "tokenLifetime": tokenLifetime}
    )
    logging.debug("data: {}".format(data))
    util.check_request( requests.post(url + "/" + __path_update, headers=headers, data=data) )

# Сменить пароль у заданного логина
def change_pass(env,login,password):
    password = __check_variable("password", password)
    url = __get_url(env)
    headers = __get_headers(env)
    data = json.dumps( 
            {"login": login,
            "newPassword": password}
    )
    logging.debug("data: {}".format(data))
    util.check_request( requests.post(url + "/" + __path_change_pass, headers=headers, data=data) )
    return password
