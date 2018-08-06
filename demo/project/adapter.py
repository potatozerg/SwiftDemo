import requests
import json
import hmac
from hashlib import sha1
from time import time

login_domain = 'https://nb.novovivo.org:5000'
point_domain = 'http://nb.novovivo.org:8080'
version_account = '/v1/AUTH_4e32fb0cc9114e23909bb6f9168e4e47'
end_point = point_domain + version_account


def login(username, password, project):
    url = login_domain + '/v3/auth/tokens'
    headers = {'content-type': "application/json"}
    body = {"auth": {"identity": {"methods": ["password"], "password": {
        "user": {"name": username, "domain": {"id": "default"}, "password": password}}},
                     "scope": {"project": {"name": project, "domain": {"id": "default"}}}}}
    # 发送请求
    response = requests.post(url, data=json.dumps(body), headers=headers)
    # 打印token
    token = response.headers['x-subject-token']
    # print(token)
    return token


def get_account_key(token):
    url = end_point
    headers = {'X-Auth-Token': token}
    # 发送请求
    response = requests.head(url, headers=headers)
    # 返回信息'Last-Modified'
    key = response.headers['X-Account-Meta-Temp-Url-Key']
    # print(key)
    return key


def create_container(token, container):
    url = end_point + "/" + container
    headers = {'Content-Length': "0", 'X-Auth-Token': token}
    # 发送请求
    response = requests.put(url, headers=headers)
    # 返回信息
    # print(response.status_code)
    return response.status_code


def delete_container(token, container):
    url = end_point + "/" + container
    headers = {'X-Auth-Token': token}
    # 发送请求
    response = requests.delete(url, headers=headers)
    # 返回信息
    # print(response.text)
    return response.text


def get_containers_list(token):
    url = end_point
    headers = {'content-type': "application/json", 'X-Auth-Token': token}
    # 发送请求
    response = requests.get(url, headers=headers)
    # 返回信息
    containers = response.text.split('\n')
    containers = [i for i in containers if len(i) > 0]
    # print(containers)
    return containers


def get_container_details(token, container):
    url = end_point + '/' + container
    headers = {'content-type': "application/json", 'X-Auth-Token': token}
    # 发送请求
    response = requests.get(url, headers=headers)
    # 返回信息'Last-Modified'
    containers = response.text.split('\n')
    containers = [i for i in containers if len(i) > 0]
    # print(containers)
    return containers


def create_object(token, container, object, data):
    url = end_point + '/' + container + '/' + object
    headers = {'X-Auth-Token': token}

    # 发送请求
    response = requests.put(url, headers=headers, files={object: data})
    # 返回信息
    # print(response.status_code)
    return response.status_code


def delete_object(token, container, object):
    url = end_point + '/' + container + '/' + object
    # url += '?multipart-manifest=delete'
    headers = {'X-Auth-Token': token}
    # 发送请求
    response = requests.delete(url, headers=headers)
    # 返回信息
    print(response.text)
    print(container)
    print(object)
    # print(response.status_code)
    return response.status_code


def get_object_content(token, container, object):
    url = end_point + '/' + container + '/' + object
    headers = {'content-type': "application/json", 'X-Auth-Token': token}
    # 发送请求
    response = requests.get(url, headers=headers)
    # 返回信息'Last-Modified'
    # print(response.text)
    return response.text


def get_object_content_temp(token, container, object):
    method = 'GET'
    duration_in_seconds = 30
    expires = int(time() + duration_in_seconds)
    path = version_account + '/' + container + '/' + object
    key = get_account_key(token=token)
    hmac_body = '%s\n%s\n%s' % (method, expires, path)
    signature = hmac.new(bytes(key, 'ascii'), hmac_body.encode("utf8"), sha1).hexdigest()
    url = end_point + '/' + container + '/' + object
    url += '?temp_url_sig=' + signature
    url += '&temp_url_expires=' + str(expires)
    # print(url)
    return url
