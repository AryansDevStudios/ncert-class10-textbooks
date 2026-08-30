import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('s18.js', 'r', encoding='utf-8', errors='ignore') as f:
    s18 = f.read()

lines18 = s18.split('\n')
print(f"Total lines in s18: {len(lines18)}")

for i in range(7000, len(lines18)):
    print(f"{i+1}: {lines18[i]}")
