# -*- coding: utf-8 -*-
import json, re, base64
from collections import Counter

def load_data():
    lines = [json.loads(l) for l in open('/Users/jiangtao/.wechat-insight/data/Tesla特特特能说.jsonl')]
    msgs = [l for l in lines if l.get('msg_type') == 1]
    return lines, msgs

lines, msgs = load_data()

# Trend data
hourly = Counter()
for m in msgs:
    hour = m['datetime'][11:13]
    hourly[int(hour)] += 1
trend_data = [[f"{h:02d}:00", hourly.get(h, 0)] for h in range(24)]

# Active stars
from collections import Counter as C
sc = C()
for m in msgs:
    sc[m.get('sender_name','未知')] += 1
stars = [[n, c] for n, c in sc.most_common(20) if c >= 10]

print(json.dumps({"trend": trend_data, "stars": stars}, ensure_ascii=False))
