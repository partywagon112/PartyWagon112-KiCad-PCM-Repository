import os
import pathlib
import datetime
import time
import platform
import subprocess

fname = './packages.json'
pstat = os.stat(fname)

res = subprocess.run(['sha256sum', fname], stdout=subprocess.PIPE, text=True)
sha256 = res.stdout.split(' ')[0]

tsf = pstat.st_mtime
ts = int(tsf)
dt = datetime.datetime.fromtimestamp(ts)

print('    "packages": {')
print('        "sha256": "%s",' % sha256)
print('        "update_time_utc": "%s",' % dt)
print('        "update_timestamp": %s,' % ts)
print('        "url": "https://raw.githubusercontent.com/g200kg/kicad-pcm-repository/main/packages.json"')
print('    }')