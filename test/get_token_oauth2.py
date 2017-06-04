# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import base64
import requests
import requests.exceptions

s = requests.Session()

print(70 * '_') # ------------------------------------------

params = {
	'email': 'xxx@cc.com',
	'password': 'xxx',
	'grant_type': 'password',
	'scope': 'role user client',
}
client_id = 'c310174d-2839-4b41-b1fa-f750f8c04fe6'
client_secret = 'd32b4e7c-51ac-4f99-8e16-739c0ac8a668'
auth_basic = base64.b64encode('{0}:{1}'.format(client_id, client_secret))
headers = {'Authorization': 'Basic {0}'.format(auth_basic)}

try:
	url = 'http://localhost:4000/oauth2/'
	r = s.get(url, params=params, headers=headers)
	if r.status_code == requests.codes.ok:
		if r.json()['success']:
			access_token = r.json()['access_token']
			expire = r.json()['expire']
			redirect_uri = r.json()['redirect_uri']
			print('access_token: {0}'.format(access_token))
			print('expire after: {0} seconds'.format(expire))
			print('redirect_uri: {0}'.format(redirect_uri))
			with open('access_token.txt', 'w') as file:
				file.write('{0}'.format(access_token))
		else:
			print r.json()['reason']

except requests.exceptions.RequestException:
	print('error reach oauth2-server.')

s.close()
