import requests

url='https://prod-140.westeurope.logic.azure.com:443/workflows/17cd138961c44b7786910d2c2eb7f336/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=lLHrVn02KE6uRPftIhZP0CAwU25FsZOoMAdVfRGmqVs'
data={
    'value':'Complicated'
}

result = requests.post(url=url,data=data)

print (result.status_code)