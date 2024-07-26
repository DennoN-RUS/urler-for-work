# coding: utf-8
import os
import requests
import src.utlis as util

__url_git="git_url"
__id_repo="repo_id"
__file_name="file_name"
__ref="main"

# Полчение хидера (gitlab_api_token)
def __get_headers():
    gitlab_api_token =  os.environ['gitlab_api_token']
    headers = {"PRIVATE-TOKEN": gitlab_api_token }
    return headers

# Получение файла из гита
def __get_file():
    headers = __get_headers()
    req = requests.get(__url_git + "/api/v4/projects/" + __id_repo + "/repository/files/" + __file_name + "/raw?ref=" + __ref,  headers=headers)
    util.check_request(req)
    mass = req.text.split()
    return mass

# Отправка файла в гит
def __put_file(file,env,login):
    headers = __get_headers()
    commit_message = "Add login from jenkins for env: " + env + " service: " + login
    payload =  {'branch': __ref, 'commit_message': commit_message, 'start_branch': __ref, 'actions[][action]': 'update', 'actions[][file_path]': __file_name, 'actions[][content]': file.read()}
    req = requests.post(__url_git + "/api/v4/projects/" + __id_repo + "/repository/commits",  headers=headers, data=payload)
    util.check_request(req)

# Получение файла из гита и заполнение из него словаря
def get_dict():
    mass = __get_file()
    my_dict = dict()
    for i in range(0,len(mass),2):
        my_dict[mass[i]] = mass[i+1]
    return my_dict

# Добавление нового логина/пароля в словарь
def add_to_dict(env,service_name,password,mydict: dict):
    mydict[service_name + '(' + env + '):'] = password
    return mydict

# Создание файла из словаря, отправка его в гит и удаление файла
def send_dict(my_dict: dict,env,login):
    temp = sorted(my_dict.items())
    file = open(__file_name, 'w')
    for i in range(0,len(temp)):
        file.write(f'{temp[i][0] + " " + temp[i][1]}\n')
    file.close()
    file = open(__file_name, 'r')
    __put_file(file,env,login)
    file.close()
    os.remove(__file_name)

