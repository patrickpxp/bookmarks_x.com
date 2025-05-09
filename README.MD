# Extract X.com bookmarks

This script extracts all your bookmarks, using PlayWright +  Chromium browser.
One JSON file is created per bookmark.

## Setup

```
git clone https://github.com/patrickpxp/bookmarks_x.com
cd bookmarks_x.com
python -m venv venv
source venv/bin/activate # on Mac/Linux
.\venv\scripts\activate.ps1 # on Windows
pip install -r requirements.txt
playwright install
```

## Run

You will be asked to login the first time . You might have to delete the state file "state.json" if your login has expired

```
python main.py
```

