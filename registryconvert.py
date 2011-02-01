#!/usr/bin/env python

import re
import sys

cols={}
for line in sys.stdin:
    if line.startswith('Threadcount'):
        l=line.split(':')
        threads=l[1].strip()
    elif line.startswith('Pallet'):
        l=line.split(':')
        pal=l[1].strip()
        l=pal.split(';')
        for col in l:
            m=re.match(r'([A-Za-z]+)=([0-9a-fA-F]{6})',col)
            if not m:
                continue
            cols[m.group(1)]='#%s'%m.group(2)
# Do them individually; replacing on the whole string might get caught
# in some of the hex strings
thr=re.findall(r'[a-zA-Z]+\d+',threads)
out=''
for t in thr:
    m=re.match(r'[a-zA-Z]+',t)
    out += t.replace(m.group(0),'(%s)'%cols[m.group(0)])

print out

