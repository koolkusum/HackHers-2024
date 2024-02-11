import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# import app
import time

SCOPES = 'https://www.googleapis.com/auth/calendar'

def main():
    
    local_time = dt.datetime.now()
    local_timezone = dt.datetime.now(dt.timezone.utc).astimezone().tzinfo
    current_time = dt.datetime.now(local_timezone)
    timezone_offset = current_time.strftime('%z')
    offset_string = list(timezone_offset)
    offset_string.insert(3, ':')
    timeZone = "".join(offset_string)
    print(timeZone)
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port = 0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials = creds)
        now = dt.datetime.now().isoformat() + "Z"
        event_result = service.events().list(calendarId = "primary", timeMin=now, maxResults = 10, singleEvents = True, orderBy = "startTime").execute()

        events = event_result.get("items", [])

        if not events:
            print("No upcoming events found!")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])


        event = {
            "summary": "Tech Career Fair",
            "location": "Busch Student Center",
            "description": "Explore job opportunities and network with top tech companies at our annual career fair.",
            "colorId": 6,
            "start": {
                "dateTime": "2024-02-12T14:00:00" + timeZone,
            },

            "end": {
                "dateTime": "2024-02-12T16:00:00" + timeZone,
            },
        }


        event = service.events().insert(calendarId = "primary", body = event).execute()
        print(f"Event Created {event.get('htmlLink')}")

    except HttpError as error:
        print("An error occurred:", error)

if __name__ == "__main__":
    main()
