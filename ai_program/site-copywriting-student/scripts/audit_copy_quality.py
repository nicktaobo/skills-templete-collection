#!/usr/bin/env python3
"""落地页文案与转化结构 最小校验脚本。用法：python scripts/audit_copy_quality.py <report.md>"""
import sys, pathlib
path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('report.md')
text = path.read_text(encoding='utf-8') if path.exists() else ''
checks = ['Headline 结果导向', 'CTA 是动词+结果', 'FAQ 首句直答', '禁用空泛 AI 味词']
missing = [c for c in checks if c.split()[0] not in text and c not in text]
base = [x for x in ['交付物','验收清单','下游交接'] if x not in text]
if base:
    print('FAIL missing sections: ' + ', '.join(base)); sys.exit(1)
print('OK 落地页文案与转化结构 report basic structure passed')
if missing:
    print('WARN review checklist manually: ' + '; '.join(missing))
