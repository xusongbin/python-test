
import re
import os

for f in os.listdir(os.getcwd()):
    if not re.match(r'.*\.DAT', f):
        continue
    fl = f.split('_')
    fe = '{}_{}_{}_{}_{}_{}_{}'.format(fl[0], fl[1], fl[3], fl[4], fl[2], fl[5], fl[6])
    os.rename(os.path.join(os.getcwd(), f), os.path.join(os.getcwd(), fe))
    print(f)
