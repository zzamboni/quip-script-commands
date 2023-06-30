#!/usr/bin/env python3

import sys
import re
import quip_utils

doc_type = None

match = re.search('quip-new-(.+)\.py', sys.argv[0])
if match:
    doc_type = match.group(1)
    print(f"doc_type = {doc_type}")

quip_utils.quip_new_doc(doc_type, sys.argv[1])
