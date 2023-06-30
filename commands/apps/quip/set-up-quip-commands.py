#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Set up Quip commands
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon /Applications/Quip.app/Contents/Resources/AppIcon.icns
# @raycast.packageName Quip utilities
# @raycast.needsConfirmation true

# Documentation:
# @raycast.description Create script commands for creating Quip documents, based on the configuration in quip_config.ini.
# @raycast.author diego_zamboni
# @raycast.authorURL https://raycast.com/diego_zamboni

import quip_utils

# Read template
cmd_template="quip-new.template.py"
with open(cmd_template, 'r') as file:
    template = file.read()

print(f"Reading quip_config.ini...")
quip_utils.readConfig()
doc_types = quip_utils.config.sections()
quip_utils.checkAPIToken('DEFAULT')
print(f"The configuration file contains the following document types: {' '.join(doc_types)}")

for type in doc_types:
    new_script = template
    filename = f"quip-new-{type}.py"
    print(f"Creating script for {type}: {filename}")
    # Replace config values in template
    template_values = {}
    for k,v in quip_utils.config[type].items():
        template_values[k] = v
    template_values['doc_type'] = type

    for k,v in template_values.items():
        template_k = "{{" + k + "}}"
        new_script = new_script.replace(template_k, v)
    with open(filename, 'w') as file:
        file.write(new_script)
