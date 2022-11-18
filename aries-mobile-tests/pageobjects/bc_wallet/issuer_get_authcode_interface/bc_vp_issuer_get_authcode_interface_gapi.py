"""
Class for interfacing with gmail client getting a IDIM Verified Person Credential certificate invitation
"""
from sys import platform
from time import sleep
from decouple import config
import re
import base64
import json
# import Google Api and supporting libraries
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class BCVPIssuerGetAuthCodeInterface():
    """This interface uses the google (gmail) api to login to the issuers email account and get the auth code for github"""

    #SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    SCOPES = ['https://mail.google.com/']
    _service = None

    def __init__(self, endpoint):
        """log in to gmail with Google API"""

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # Get the token.json from the secret/environment var
        token_json = json.loads(config('GOOGLE_API_TOKEN'))
        # if os.path.exists('token.json'):
        #     creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        creds = Credentials.from_authorized_user_info(token_json, self.SCOPES)

        # The following may not be needed, will have to expect the credential are valid above.
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Get the credentials.json from the secret/environment var
                credentials_json = json.loads(config('GOOGLE_API_CREDENTIALS'))
                # flow = InstalledAppFlow.from_client_secrets_file(
                #     'credentials.json', self.SCOPES)
                flow = InstalledAppFlow.from_client_secrets(
                    credentials_json, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Create the Gmail API service resource
            self._service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            raise Exception(
                f"Could not initialize gmail api service {error}")


    def get_auth_code(self):

        # delete	DELETE /gmail/v1/users/{userId}/messages/{id}
        # Immediately and permanently deletes the specified message.
        # get	GET /gmail/v1/users/{userId}/messages/{id}
        # Gets the specified message.

        # request a list of all the messages
        # wait a few seconds to wait for the verify email to come in. Change this to loop messages again 
        sleep(5)
        result = self._service.users().messages().list(userId='me').execute()
    
        # We can also pass maxResults to get any number of emails. Like this:
        # result = service.users().messages().list(maxResults=200, userId='me').execute()
        messages = result.get('messages')
    
        # messages is a list of dictionaries where each dictionary contains a message id.
    
        # iterate through all the messages
        for msg in messages:
            # Get the message from its id
            txt = self._service.users().messages().get(userId='me', id=msg['id']).execute()
    
            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']
    
                # Look for Subject and Sender Email in the headers
                for header in headers:
                    if header['name'] == 'Subject':
                        subject = header['value']
                    if header['name'] == 'From':
                        sender = header['value']
                
                if subject == "[GitHub] Please verify your device" and sender == "GitHub <noreply@github.com>":
                    # The Body of the message is in Encrypted format. So, we have to decode it.
                    # Get the data and decode it with base 64 decoder.
                    data = payload['body']['data']
                    decoded_data = base64.b64decode(data)
    
        
                    auth_code = re.sub("\D", "", str(decoded_data))

                    # Delete the email. 
                    try:
                        self._service.users().messages().delete(userId='me', id=msg['id']).execute()
                    except Exception as error:
                        raise Exception(
                            f"Could not delete verification code email with gmail api service {error}")

                    return auth_code

            except:
                raise
