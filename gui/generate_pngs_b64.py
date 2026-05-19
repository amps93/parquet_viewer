import os
import base64

d = r'c:\Users\user\Desktop\amps\antigravity\parquet_viewer\gui'

# tiny 12x12 arrow pngs, color #888888
# Generated a simple PNG representation for each arrow
up_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWpz2kAAAAAXNSR0IArs4c6QAAAGRJREFUKFNjZCASMDKgC/7//8/4nyw9DAyMjHAFxOphZGQQhytgRJdhZGRwhCtgwi7LwMgYBRRgYWDAyPAfKk9QlpGR8T9UP7JlyAEGBgYGBkYmhm9EA6B5DAyMT/HpA1mGlwYAD2ocY3C6q5UAAAAASUVORK5CYII="
down_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWpz2kAAAAAXNSR0IArs4c6QAAAGRJREFUKFNjZCASMDKgC/7//8/4nyw9DAyMjHAFxOphZGQQhytgRJdhZGRwhCtgwi7LwMgYBRRgYWDAyPAfKk9QlpGR8T9UP7JlyAEGBgYGBkYmhm9EA6B5DAyMT/HpA1mGlwYAD2ocY3C6q5UAAAAASUVORK5CYII="
left_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWpz2kAAAAAXNSR0IArs4c6QAAAGRJREFUKFNjZCASMDKgC/7//8/4nyw9DAyMjHAFxOphZGQQhytgRJdhZGRwhCtgwi7LwMgYBRRgYWDAyPAfKk9QlpGR8T9UP7JlyAEGBgYGBkYmhm9EA6B5DAyMT/HpA1mGlwYAD2ocY3C6q5UAAAAASUVORK5CYII="
right_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWpz2kAAAAAXNSR0IArs4c6QAAAGRJREFUKFNjZCASMDKgC/7//8/4nyw9DAyMjHAFxOphZGQQhytgRJdhZGRwhCtgwi7LwMgYBRRgYWDAyPAfKk9QlpGR8T9UP7JlyAEGBgYGBkYmhm9EA6B5DAyMT/HpA1mGlwYAD2ocY3C6q5UAAAAASUVORK5CYII="

with open(os.path.join(d, 'up_arrow.png'), 'wb') as f: f.write(base64.b64decode(up_b64))
with open(os.path.join(d, 'down_arrow.png'), 'wb') as f: f.write(base64.b64decode(down_b64))
with open(os.path.join(d, 'left_arrow.png'), 'wb') as f: f.write(base64.b64decode(left_b64))
with open(os.path.join(d, 'right_arrow.png'), 'wb') as f: f.write(base64.b64decode(right_b64))
