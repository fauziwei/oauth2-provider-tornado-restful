# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import requests
import requests.exceptions

s = requests.Session()

print(70 * '_') # ------------------------------------------

params = {
	'client_id': 'c310174d-2839-4b41-b1fa-f750f8c04fe6'
}

with open('access_token.txt') as file:
	rows = file.readlines()
	row = rows[0]
	row = row[:-1] if row.endswith('\n') else row

access_token = row
headers = { 'Authorization': access_token }

try:
	url = 'http://localhost:4000/client/'
	# r = s.get(url, params=params, headers=headers)
	r = s.get(url, headers=headers)
	if r.status_code == requests.codes.ok:
		print(r.json()['clients'])

except requests.exceptions.RequestException:
	print('error reach oauth2-server.')

s.close()
