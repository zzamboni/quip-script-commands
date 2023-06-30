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

quip_utils.quip_new_doc('note', sys.argv[1])
