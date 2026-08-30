import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('s17.js', 'r', encoding='utf-8', errors='ignore') as f:
    s17 = f.read()

# Find change1 start
idx = s17.find('function change1')
print("change1 index:", idx)
print("Preview of change1:")
print(s17[idx:idx+2500])
