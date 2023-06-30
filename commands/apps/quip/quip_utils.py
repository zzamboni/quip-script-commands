#!/usr/bin/env python3

import quip
import os
import sys
import subprocess
from datetime import datetime
import configparser

config = None
config_file = "quip_config.ini"

def fail(message):
    print(message)
    sys.exit(1)

# Read configuration
def readConfig(filename=config_file):
    global config
    config = configparser.ConfigParser()
    files_read = config.read(filename)
    if filename not in files_read:
        fail(f"Could not read config file '{filename}'.")

def checkAPIToken(doc_type):
    if config[doc_type].get('APIToken', "") == "":
        fail(f"Error: Please configure APIToken in {config_file}.")

# Function from https://gist.github.com/XuankangLin/7ec82f80a0044a52330720244de2d15a
def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

def quip_new_doc(doc_type, title):
    readConfig()
    if not config.has_section(doc_type):
        fail(f"Error: Quip document type '{doc_type}' is not defined in {config_file}.")
    checkAPIToken(doc_type)

    try:
        client = quip.QuipClient(access_token=config[doc_type]['APIToken'], base_url=config[doc_type]['APIURL'])
        if config[doc_type].getboolean('PrependDate'):
            title = datetime.now().strftime("%Y-%m-%d") + " " + title

        # print(f"Creating new note '{title}' in folder {folder_id}...")
        folders = []
        if config[doc_type].get('FolderID',None):
            folders = [config[doc_type].get('FolderID',None)]
        result = client.new_document(content=title, format="markdown", member_ids=folders)
    except Exception as e:
        if e.code == 401:
            fail(f"Please configure/verify your Quip API token in {config_file}")
        elif e.code == 400:
            fail(f"Please configure/verify folder ID for [{doc_type}] in {config_file}")
        else:
            fail(f"Received a Quip error:", e, file=sys.stderr)

    if result:
        url = result['thread']['link']
        if url:
            print(f"New {doc_type} created", end="")
            if config[doc_type].getboolean('CopyURLToClipboard'):
                setClipboardData(url.encode('utf_8'))
                print(f", URL copied to clipboard", end="")

            if config[doc_type].getboolean('OpenDocs'):
                print(f", opening {url}", end="")
                app_args=[]
                if config[doc_type].getboolean('UseQuipApp'):
                    app_args=["-a", "Quip"]
                try:
                    open_args=["/usr/bin/open", *app_args, url]
                    # print(f"Running {open_args}")
                    # We use Popen to put the open process in the background.
                    pid = subprocess.Popen(open_args).pid
                except OSError as e:
                    print("Execution failed:", e, file=sys.stderr)
            print(".")
        else:
            fail(f"Something went wrong, could not create document.")
