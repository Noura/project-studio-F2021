import requests

response = requests.get('http://192.168.1.76:5000/')
print('response status code', response.status_code)
print('response content', response.content)
