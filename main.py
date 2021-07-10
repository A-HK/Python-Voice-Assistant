#for Google Calendar API
from __future__ import print_function #__future__ module always needs to be at beginning of program
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#for Google Text to Speech
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] #good practice to have all global variables at top

#output audio
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename="voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


#getting input audio from user (converting user voice to text)
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source: #could also use textfile as source
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio) #uses google api to recognize what user says
            print(said)
        except Exception as e:
            print("Exception:" + str(e))

        return said

#speak("Hello") if you want Google TTS to speak to user
#text = get_audio()

#if "hello" in text:
    #speak("Hello, how are you?")
#if "My name is Luke" in text:
    #speak("Luke, I am your father!")



def authenticate_google_cal():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service

    # Call the Calendar API
def get_event(service, n):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the {n} upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

service = authenticate_google_cal()
get_event(service, 2)
#if __name__ == '__main__':
    #main()
