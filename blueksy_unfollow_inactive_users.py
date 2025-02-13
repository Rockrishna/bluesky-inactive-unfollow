"""
AT.py

Description:
    This script logs into a Bluesky account, retrieves profile and follow information,
    monitors user activity based on their latest posts, and unfollows users who appear inactive
    (no posts or posts older than a month).

Expected Usage:
    1. Ensure required packages (json, atproto, datetime, getpass) are installed.
    2. Run the script and enter your Bluesky credentials when prompted.
    3. Run the script from the command line: python AT.py

"""
import json
from atproto import Client
from datetime import datetime
from getpass import getpass

def get_credentials():
    """Prompt user for Bluesky credentials"""
    print("Please enter your Bluesky credentials:")
    username = input("Username: ")
    password = getpass("Password: ")
    return username, password

# Get credentials from user
username, password = get_credentials()

# Initialize client and login
client = Client()
try:
    session = client.login(username, password)
    data = client.get_profile(actor=username)
except Exception as e:
    print(f"Login failed: {str(e)}")
    exit(1)
#notify that the login was successful
print("Login successful")
# Function: get_handles
# Retrieves a list of handles from the current user's follows.
def get_handles():
    follows = client.get_follows(actor=data.did, limit=100)
    handles = [profile['handle'] for profile in follows['follows']]
    return handles

# Function: has_two_months_passed
# Checks if at least two months have passed since the given date.
def has_two_months_passed(date_str):
    date_format = "%Y-%m-%d"
    input_date = datetime.strptime(date_str, date_format).date()
    today = datetime.today().date()
    year_diff = today.year - input_date.year
    month_diff = today.month - input_date.month + year_diff * 12
    return month_diff >= 2

## Function: unfollow_user
## Unfollows a specified user by handle if they exist in the follows list.
def unfollow_user(handle_to_unfollow):
    """
    Unfollow a user on Bluesky by their handle.

    Args:
        handle_to_unfollow: The handle of the user you want to unfollow.

    Returns:
        str: A success or error message.
    """
    try:
        handles = get_handles()
        
        if handle_to_unfollow not in handles:
            return f"Error: {handle_to_unfollow} is not in your following list."

        follows = client.get_follows(actor=data.did, limit=100)

        follow_record = None
        for follow in follows['follows']:
            if follow.handle == handle_to_unfollow:  # Access the 'handle' attribute directly
                follow_record = follow.viewer.following  # Get the following record URI
                break

        if not follow_record:
            return f"Error: No follow record found for {handle_to_unfollow}."

        client.delete_follow(follow_record)
        return f"Successfully unfollowed {handle_to_unfollow}."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- Main Execution Loop ---
# Initialize the cache and process each handle to check for inactivity.
checked_handles = []
a = True
while a:
    old_handles = get_handles()
    for i in old_handles:
        if i in checked_handles:
            continue
        # Retrieve the most recent post from each followed user
        post = client.get_author_feed(actor=i, limit=1)
        # Attempt to extract the post creation date
        try:
            date = post["feed"][0]["post"]["record"]["created_at"].split("T")[0]
        except:
            print(f"0 posts on the following handle: {i}. Unfollowing")
            print(unfollow_user(i))
            date = datetime.today().date().strftime("%Y-%m-%d")
        # Check if the user has been inactive (based on post date)
        if has_two_months_passed(date):
            print(f"At least two months has passed, unfollowing {i}")
            print(unfollow_user(i))
        checked_handles.append(i)

    handles = get_handles()
    if old_handles == handles:
        print("Handles are the same, exiting")
        a = False
print("Complete")