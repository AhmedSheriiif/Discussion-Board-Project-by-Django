import requests

url = "http://localhost:8000/apis/test/board-details-queryset"


# headers = {'Content-Type': "application/json"}
params = {'id': [1, 2]}


response = requests.get(url, params=params)

print(response)
print(response.json())
