import getpass
from datetime import date

from garminconnect import Garmin, GarminConnectAuthenticationError

TOKEN_STORE = "~/.garminconnect"


def get_client() -> Garmin:
    """Return an authenticated Garmin client."""
    client = Garmin(None, None, prompt_mfa=lambda: input("Enter MFA Code: "))

    try:
        client.login(tokenstore=TOKEN_STORE)
    except GarminConnectAuthenticationError:
        print("Unable to retrieve cached tokens, logging in")
        email = input("Garmin Email: ")
        pw = getpass.getpass("Garmin Password: ")
        client = Garmin(email, pw, prompt_mfa=lambda: input("Enter MFA Code: "))
        client.login(tokenstore=TOKEN_STORE)

    return client


def fetch_day(client: Garmin, day: date) -> dict:
    """Return raw Garmin data for one day."""
    iso = day.isoformat()
    stats = client.get_stats(iso)
    sleep = client.get_sleep_data(iso)["dailySleepDTO"]
    return {
        "steps": stats["totalSteps"],
        "sleep_start": sleep["sleepStartTimestampLocal"],
        "sleep_end": sleep["sleepEndTimestampLocal"],
    }


if __name__ == "__main__":
    c = get_client()
    today = date.today()
    print(fetch_day(c, today))
