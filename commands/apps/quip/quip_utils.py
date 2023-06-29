#!/usr/bin/env python3

import quip
import os
import sys
import subprocess
from datetime import datetime

try:
    from quip_config import *
except ModuleNotFoundError:
    print(f"Please configure quip_config.template.py and rename it to quip_config.py")
    sys.exit(1)

# Function from https://gist.github.com/XuankangLin/7ec82f80a0044a52330720244de2d15a
def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

def quip_new_doc(folder_id, title, add_date=False):
    now = datetime.now() # current date and time
    nowstr = now.strftime("%Y-%m-%d") + " "

    try:
        client = quip.QuipClient(access_token=QUIP_TOKEN, base_url=QUIP_URL)
        if add_date:
            title = nowstr + title

        # print(f"Creating new note '{title}' in folder {folder_id}...")
        result = client.new_document(content=title, format="markdown", member_ids=[folder_id])
    except Exception as e:
        if e.code == 401:
            print(f"Please configure/verify your Quip API token in quip_config.py")
        elif e.code == 400:
            print(f"Please configure/verify folder ID '{folder_id}' in quip_config.py")
        else:
            print(f"Received a Quip error:", e, file=sys.stderr)
        sys.exit(1)

    if result:
        url = result['thread']['link']
        if url:
            if QUIP_COPY_URL_TO_CLIPBOARD:
                setClipboardData(url.encode('utf_8'))
                print(f"New note created. URL copied to clipboard.")
            else:
                print(f"New note created.")

            if QUIP_OPEN:
                print(f"New note created, opening {url}.")
                app_args=[]
                if QUIP_USE_APP:
                    app_args=["-a", "Quip"]
                try:
                    open_args=["/usr/bin/open", *app_args, url]
                    # print(f"Running {open_args}")
                    # We use Popen to put the open process in the background.
                    pid = subprocess.Popen(open_args).pid
                except OSError as e:
                    print("Execution failed:", e, file=sys.stderr)
        else:
            print(f"Something went wrong, could not create document.")
            sys.exit(1)
