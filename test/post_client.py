# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import uuid
import requests
import requests.exceptions

s = requests.Session()

print(70 * '_') # ------------------------------------------

# Make it permanents for this 1 App.
params = {
	'name': 'production_tool'
}

with open('access_token.txt') as file:
	rows = file.readlines()
	row = rows[0]
	row = row[:-1] if row.endswith('\n') else row

access_token = row
headers = { 'Authorization': access_token }

try:
	url = 'http://localhost:4000/client/'
	r = s.post(url, params=params, headers=headers)
	if r.status_code == requests.codes.ok:
		print(r.json()['success'])

except requests.exceptions.RequestException:
	print('error reach oauth2-server.')

s.close()
