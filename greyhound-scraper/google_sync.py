from __future__ import print_function
import httplib2
import os
import argparse

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json

# available scopres are available here: https://developers.google.com/sheets/api/guides/authorizing#OAuth2Authorizing
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Greyhound Canada Scraper'

def get_credentials(flags):
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-greyhound-canada-scraper.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

if __name__ == "__main__":
	parser = argparse.ArgumentParser(parents=[tools.argparser], description="Writes schedules to a google sheet.")
	parser.add_argument("--sheet-id", "-s", dest="sheet_id", help="the google sheet ID", required=True)
	args = parser.parse_args()

	credentials = get_credentials(args)
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

	#read from the spreedsheet
	result = service.spreadsheets().values().get(spreadsheetId=args.sheet_id, range="A1").execute()
	print(result)

	#write to the spreedsheet
	values = [
		["BBB", "CCC"]
	]
	body = {
		'values': values
	}
	result = service.spreadsheets().values().update(spreadsheetId=args.sheet_id, range="A1:B1", body=body, valueInputOption="RAW").execute()

