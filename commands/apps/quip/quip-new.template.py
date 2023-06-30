#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title {{title}}
# @raycast.mode compact

# Optional parameters:
# @raycast.icon /Applications/Quip.app/Contents/Resources/AppIcon.icns
# @raycast.argument1 { "type": "text", "placeholder": "{{arg_placeholder}}" }
# @raycast.packageName Quip utilities

# Documentation:
# @raycast.description Configure your Quip API token and other defaults in quip_config.ini
# @raycast.author zzamboni
# @raycast.authorURL https://raycast.com/zzamboni

import sys

import quip_utils

quip_utils.quip_new_doc('{{doc_type}}', sys.argv[1])
