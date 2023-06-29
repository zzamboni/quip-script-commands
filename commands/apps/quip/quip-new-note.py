#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title New Quip note
# @raycast.mode compact

# Optional parameters:
# @raycast.icon /Applications/Quip.app/Contents/Resources/AppIcon.icns
# @raycast.argument1 { "type": "text", "placeholder": "Note title" }
# @raycast.packageName Quip utilities

# Documentation:
# @raycast.description Create a new note in Quip. Configure your Quip API token and other defaults in quip_config.py
# @raycast.author zzamboni
# @raycast.authorURL https://raycast.com/zzamboni

import sys

import quip_utils

try:
    import quip_config
except ModuleNotFoundError:
    print(f"Please configure quip_config.template.py and rename it to quip_config.py")
    sys.exit(1)

folder_id = quip_config.QUIP_NOTES_ID
title = sys.argv[1]
add_date = quip_config.QUIP_NOTES_PREPEND_DATE

quip_utils.quip_new_doc(folder_id, title, add_date)
