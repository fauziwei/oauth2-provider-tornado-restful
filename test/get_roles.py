# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import requests
import requests.exceptions

s = requests.Session()

print(70 * '_') # ------------------------------------------

params = { 'role_id': 'dbd67d8a-d8d9-41e6-bade-6352110a479a' }

with open('access_token.txt') as file:
	rows = file.readlines()
	row = rows[0]
	row = row[:-1] if row.endswith('\n') else row

access_token = row
headers = { 'Authorization': access_token }

try:
	url = 'http://localhost:4000/role/'
	# r = s.get(url, params=params, headers=headers)
	r = s.get(url, headers=headers)
	if r.status_code == requests.codes.ok:
		print(r.json()['roles'])

except requests.exceptions.RequestException:
	print('error reach oauth2-server.')

s.close()
