# 📬 Gmail Email Cleaner

A Python tool to search and delete old Gmail messages older than 2 years using the Gmail API.  
Great for decluttering inboxes with large volumes of old, unread, or unnecessary messages.

---

## ✨ Features

- Authenticates with your Gmail account using OAuth 2.0
- Searches for emails older than a given date
- Prints **Subject** and **Date Received** for each email
- Counts total emails found
- Deletes emails in bulk (optional)
- Fully configurable and extendable

---

## 🛠 Requirements

- Python 3.7+
- Gmail API enabled in Google Cloud Console
- OAuth 2.0 credentials (`credentials.json`)
- A Gmail account with messages to clean

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/donadley/GmailEmailCleaner.git
cd GmailEmailCleaner


2. Create and activate a virtual environment (optional)

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt


4. Set up Gmail API

 - Go to the Google Cloud Console
 - Enable the Gmail API
 - Create OAuth 2.0 credentials for a Desktop app
 - Download the credentials.json and place it in the project folde

5. Running the App
python emailCleanup.py
```

*You'll be prompted to authorize access in your browser the first time you run it.
After that, it will scan for emails older than 2 years, list the subject lines and dates, and optionally delete them.*

---


## Configuration

You can customize the number of days to look back (default is 730 days = 2 years) by changing:

age_in_days = 730

You can also adjust the Gmail search query in the code if you want to add more filters (like label, sender, unread, etc.)

## Warning

This script can delete emails, so use it carefully.
Make sure you’re not deleting important messages.

## License

MIT License


## Contact

Created by @donadley
Questions or suggestions? Feel free to open an issue or contribute!
---

Let me know if you want to add:
- Screenshots or terminal examples
- An option to archive instead of delete
- CSV export of email subjects and dates

Happy cleaning! 🧹📫