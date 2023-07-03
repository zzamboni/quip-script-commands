#!/usr/bin/env python3
#
# Utility library for interacting with the Quip API and for other common
# functions.
#
# Diego Zamboni <diego@zzamboni.org>

import quip
import os
import sys
import subprocess
from datetime import datetime
import configparser

config = None
config_file = "quip_config.ini"

# Print error message and exit with a non-zero code.
def fail(message):
    red = "\u001b[31m"
    print(red + message)
    sys.exit(1)

# Read configuration file into global config variable.
def readConfig(filename=config_file):
    global config
    config = configparser.ConfigParser()
    files_read = config.read(filename)
    if filename not in files_read:
        fail(f"Could not read config file '{filename}'.")

# Check whether the APIToken field has a non-empty value and exit if it doesn't.
# Does not verify that it's valid.
def checkAPIToken(doc_type):
    if config[doc_type].get('APIToken', "") == "":
        fail(f"Error: Please configure APIToken in {config_file}.")

# Put a string in the macOS clipboard using the pbcopy command.
#
# Function originally from
# https://gist.github.com/XuankangLin/7ec82f80a0044a52330720244de2d15a modified
# to automatically call encode('utf_8') on its argument, with the assumption
# that it's a string.
def setClipboardData(text):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(text.encode('utf_8'))
    p.stdin.close()
    retcode = p.wait()

# Create a new document in Quip.
#
# The document is created according to the configuration associated with the
# given doc_type. This indicates parameters such as the APIToken to use, whether
# to prepend the current date to the text, and the folder in which the document
# should be stored. See quip_config.ini for the full list of available
# configuration parameters.
#
def quip_new_doc(doc_type, text):
    readConfig()
    if not config.has_section(doc_type):
        fail(f"Error: Quip document type '{doc_type}' is not defined in {config_file}.")
    checkAPIToken(doc_type)

    # Prepend date to the text if needed
    if config[doc_type].getboolean('PrependDate'):
        dateformat = config[doc_type].get('DateFormat', "%Y-%m-%d")
        text = datetime.now().strftime(dateformat) + " " + text

    # What to do?
    action = config[doc_type].get('action', 'create')

    try:
        client = quip.QuipClient(access_token=config[doc_type]['APIToken'], base_url=config[doc_type]['APIURL'])

        if action == 'create':
            # print(f"Creating new note '{text}' in folder {folder_id}...")
            folders = []
            folderID = config[doc_type].get('FolderID',None)
            if folderID:
                folders = [folderID]
            templateID = config[doc_type].get('TemplateID', None)
            # If TemplateID is given, use it to create the doc, otherwise create an empty one
            if templateID:
                result = client.copy_document(templateID, folder_ids=[folderID], title=text)
            else:
                result = client.new_document(content=text, format="markdown", member_ids=folders)
        elif action == 'add':
            listmarkup = { "todo": "[] ", "bullet": "- ", "num": "1. " }
            listtype = config[doc_type].get('ListType', 'none')
            docid = config[doc_type].get('DocID', None)
            if not docid:
                fail(f"Error: no DocID provided, needed for 'add' action.")
            if listtype in listmarkup:
                text = listmarkup[listtype] + text
            result = client.edit_document(docid, text, format='markdown', section_id='')
        else:
            fail(f"Error: Invalid action value '{action}', should be 'create' or 'add'.")

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
                setClipboardData(url)
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
            fail(f"Something went wrong, could not get the document URL.")
    else:
        fail(f"Something went wrong, could not create document.")
