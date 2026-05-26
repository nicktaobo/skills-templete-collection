#!/usr/bin/env python3
import sys, pathlib, re
path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('HANDOFF.md')
text = path.read_text(encoding='utf-8') if path.exists() else ''
required = ['[DONE]', '交付物', '质量门槛', '下游交接']
missing = [x for x in required if x not in text]
if missing:
    print('FAIL missing: ' + ', '.join(missing))
    sys.exit(1)
print('OK handoff looks complete')
