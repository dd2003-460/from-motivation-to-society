import os
import re

with open('main.tex', 'r') as f:
    content = f.read()

subfiles = re.findall(r'\\subfile\{(.*?)\}', content)
for sf in subfiles:
    if not sf.endswith('.tex'):
        sf_path = sf + '.tex'
    else:
        sf_path = sf
    
    if os.path.exists(sf_path):
        print(f"EXISTS: {sf_path}")
    else:
        print(f"MISSING: {sf_path}")
