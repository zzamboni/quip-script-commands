#!/usr/bin/env python3

### Base configuration

# Quip base URL to use
QUIP_BASE='https://quip.com/'
# Quip API URL to use
QUIP_URL='https://platform.quip.com'

### Behavior configuration

# Prepend date to title of new "notes"?
QUIP_NOTES_PREPEND_DATE=True
# Prepend date to title of new "meeting notes"?
QUIP_MEETNOTES_PREPEND_DATE=True

# Whether to automatically open the created documents.
QUIP_OPEN=True
# Whether to copy the URL of newly created documents to the clipboard
QUIP_COPY_URL_TO_CLIPBOARD=False
# Whether to open documents in the app or in the browser
QUIP_USE_APP=True

### Personal configuration
##
## The document/folder IDs can be obtained by using the "Copy Link" menu
## option in Quip. The ID is the part that comes right after the hostname
## in the URL. For example: https://quip.com/A7RmAB1oNeuL

# Quip API token. Get one at https://quip.com/api/personal-token
QUIP_TOKEN='YOUR_QUIP_API_TOKEN'

# Default folder in Quip where to create notes
QUIP_NOTES_ID='YOUR_QUIP_NOTES_FOLDER'
# Folder in which to create meeting notes
QUIP_MEETNOTES_ID='YOUR_QUIP_MEETING_NOTES_FOLDER'
