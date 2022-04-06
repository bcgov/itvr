from ftplib import FTP
from io import StringIO
import re

import sys

# Connect to local ftp server
ftp = FTP(host='localhost', user='user',passwd='1234')

###################### Download ###########################
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

# Download all files
for line in listing:
  file = re.findall('.* (.*)',line)[0]
  localfile = open(file, 'wb')
  ftp.retrbinary('RETR ' + file,localfile.write, 1024)
#########################################################


###################### Upload ###########################
# Upload a file
filename = 'uploadme.txt'
ftp.storbinary('STOR '+filename, open(filename,'rb'))
#########################################################


# Close connection
ftp.close()