import codecs
import gzip
import os
import sys

import urllib.parse as urlparse

rep = '' if len(sys.argv) < 4 else sys.argv[3].strip()

zf = gzip.open(os.path.abspath(sys.argv[1]), 'r')
# reader = codecs.getreader("utf-8")
# contents = reader( zf )

writer = codecs.open(os.path.abspath(sys.argv[2]), 'w')

c = 0
for line in zf:
    try:
        out = ' '.join([e if not urlparse.urlparse(e).scheme else rep for e in line.split()])
    except:
        out = line.strip()
    out = ' '.join([e for e in out.split() if not e.startswith('@')])
    out = ' '.join([e for e in out.split() if not e.startswith('@')])
    out = ' '.join([e for e in out.split() if not e.startswith('#')])
    out = out.replace("[[", "").replace("]]", "")
    # out = out.replace('&quot;','"').replace('&amp;','\'').replace('&lt;','<').replace('&gt;','>')
    writer.write(out + '\n')
    c += 1
    if c % 10000 == 0: sys.stdout.write(str(c) + '...')

writer.close()
print('gzipping...')

os.system('gzip ' + os.path.abspath(sys.argv[2]))
print('done!')
