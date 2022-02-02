from ftplib import FTP
from io import StringIO
import re

import sys

ftp = FTP(host='localhost', user='user',passwd='1234')

# Store output for later
old_stdout = sys.stdout

# Redirect output
result = StringIO()
sys.stdout = result

# Print listing of files
ftp.dir()

# Reset standard output
sys.stdout = old_stdout

# Grab the string and create array of files
listing = result.getvalue().splitlines()


for line in listing:
  file = re.findall('.* (.*)',line)[0]
  print(file)

# Close connection
ftp.close()