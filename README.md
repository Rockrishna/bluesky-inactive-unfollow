# Bluesky Inactive User Unfollower

A Python script that helps manage your Bluesky social media follows by automatically unfollowing users who have been inactive for more than two months.

## Features

- Automatic login to Bluesky account
- Retrieves and processes your following list
- Identifies inactive users based on:
  - Users with no posts
  - Users whose last post is older than 2 months
- Automatically unfollows inactive users
- Secure password input using getpass
- Progress tracking to avoid rechecking the same users

## Prerequisites

- Python 3.x
- Required Python packages:
  - atproto
  - datetime
  - getpass
  - json

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python blueksy_unfollow_inactive_users.py
```

2. When prompted, enter your Bluesky:
   - Username
   - Password (input will be hidden for security)

3. The script will:
   - Log into your account
   - Process your following list
   - Automatically unfollow inactive users
   - Display progress and results in the console

## How It Works

The script performs the following operations:
1. Authenticates with Bluesky using provided credentials
2. Retrieves the list of accounts you follow
3. For each followed account:
   - Checks their most recent post
   - If they have no posts, unfollows them
   - If their last post is older than 2 months, unfollows them
4. Keeps track of processed accounts to avoid redundant checks

## Security Note

- Your credentials are never stored and are only used for the current session
- Password input is masked during entry for security
- The script uses the official atproto client for Bluesky interactions

## Project Structure

```
Bluesky-Project/
├── Bluesky-backend/
│   └── blueksy_unfollow_inactive_users.py
├── Bluesky-frontend/
│   └── main.py
├── Credentials.txt
├── requirements.txt
└── README.md
```

## Contributing

Feel free to submit issues and enhancement requests!