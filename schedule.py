#!/usr/bin/env python2
import ConfigParser
from StringIO import StringIO
import smtplib
import imaplib
import email
import re
from dateutil.parser import parse as parse_datetime
from datetime import datetime

DEFAULT_CONFIG = """\
[smtp]
host=smtp.googlemail.com

[imap]
host=imap.googlemail.com
drafts=[Google Mail]/Entw&APw-rfe
"""


config = ConfigParser.ConfigParser()
config.readfp(StringIO(DEFAULT_CONFIG))
config.read('schedule.cfg')

smtp = smtplib.SMTP_SSL(config.get('smtp', 'host'))
smtp.login(config.get('smtp', 'user'), config.get('smtp', 'pass'))

imap = imaplib.IMAP4_SSL(config.get('imap', 'host'))
imap.login(config.get('imap', 'user'), config.get('imap', 'pass'))

imap.select(config.get('imap', 'drafts'))

res, data = imap.search(None, 'ALL')
res, msg_data = imap.fetch(data[0].replace(' ', ','), '(RFC822)')

for line in msg_data:
    if isinstance(line, tuple):
        mail = email.message_from_string(line[1])
        if mail['Subject'].find('|') >= 0:
            msg_id = line[0].split()[0]
            date = parse_datetime(mail['Subject'][:mail['Subject'].find('|')], dayfirst=True)
            print date
            if date <= datetime.now():
                del mail['Message-ID']
                subject = mail['Subject'][mail['Subject'].find('|') + 1:].strip()
                del mail['Subject']
                mail['Subject'] = subject
                smtp.sendmail(mail['From'], mail['To'], mail.as_string())
                imap.store(msg_id, '+FLAGS', r'(\Deleted)')

imap.expunge()

try:
    imap.close()
except:
    pass
try:
    imap.logout()
except:
    pass
try:
    smtp.quit()
except:
    pass
