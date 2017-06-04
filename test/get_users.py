# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import requests
import requests.exceptions

s = requests.Session()

print(70 * '_') # ------------------------------------------

params = {
	# 'user_id': '7329d1e5-edd4-4d04-8ea8-090ee72ed880'
	'user_id': 'ef81661f-069e-42a4-839e-602ca473dff4'
}

with open('access_token.txt') as file:
	rows = file.readlines()
	row = rows[0]
	row = row[:-1] if row.endswith('\n') else row

access_token = row
headers = { 'Authorization': access_token }

try:
	url = 'http://localhost:4000/user/'
	# r = s.get(url, params=params, headers=headers)
	r = s.get(url, headers=headers)
	if r.status_code == requests.codes.ok:
		print(r.json()['users'])

except requests.exceptions.RequestException:
	print('error reach oauth2-server.')

s.close()
