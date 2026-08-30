import re
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('textbook_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    raw = f.read()

scripts = re.findall(r'<script.*?>.*?</script>', raw, re.DOTALL | re.IGNORECASE)

s17 = scripts[17]
s18 = scripts[18]

# Save s17 and s18 to disk for detailed inspection
with open('s17.js', 'w', encoding='utf-8') as f:
    f.write(s17)

with open('s18.js', 'w', encoding='utf-8') as f:
    f.write(s18)

print("Saved s17.js (length {}) and s18.js (length {})".format(len(s17), len(s18)))

# Let's find forms
forms = re.findall(r'<form.*?</form>', raw, re.DOTALL | re.IGNORECASE)
for i, fm in enumerate(forms):
    print(f"\n--- FORM {i} ---")
    print(fm)
