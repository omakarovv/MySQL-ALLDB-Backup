#!/usr/bin/env python
import ConfigParser # install from PIP for Python 2.7: pip install ConfigParser
import os
import time
import shutil

# On Debian, /etc/mysql/debian.cnf contains 'root' a like login and password.

config = ConfigParser.ConfigParser()
config.read("/root/debian.cnf")
username = config.get('client', 'user')
password = config.get('client', 'password')
hostname = config.get('client', 'host')
filestamp = time.strftime('%Y-%m-%d-%H:%M:%S')

# Variables
DBBACKUPPATH = '/home/backup/dbbackup'

tarcmd = ("tar -czf /home/backup/ALLDB." +
          filestamp + ".tar.gz" " " + DBBACKUPPATH + "/")

# Check DBBACKUPPATH. /home/backup - must be created.
dir_exist = os.path.exists('/home/backup/dbbackup')

if dir_exist is True:
    shutil.rmtree(DBBACKUPPATH)
    os.mkdir(DBBACKUPPATH)
else:
    os.mkdir(DBBACKUPPATH)

tarcmd = ("tar -czf /home/backup/ALLDB." +
          filestamp + ".tar.gz" " " + DBBACKUPPATH + "/")

# Get a list of databases:

database_list_command = (
                     "mysql -u %s -p%s -h %s --silent -N -e 'show databases'"
                     % (username, password, hostname)
                     )

for database in os.popen(database_list_command).readlines():
    database = database.strip()

    if database in ['information_schema', 'performance_schema']:
        continue

    filename = "/home/backup/dbbackup/%s-%s.sql" % (database, filestamp)
    os.popen(("mysqldump -u %s -p%s -h %s -e --opt -c %s > %s"
             % (username, password, hostname, database, filename)))

# ALL DB BACKUP
os.system(tarcmd)

# Delete tmp backup dir
shutil.rmtree(DBBACKUPPATH)
