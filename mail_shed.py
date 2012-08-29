#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__version__ = '0.1'

import argparse
import os


#==============================================================================
# Command line argument parser
#==============================================================================

# Create parser
argparser = argparse.ArgumentParser(
    description='Send emails from imap draft folder which should have been '
                'sent by now.',
    epilog='Options given via command line are preferred '
           'over options set in config file. IMAP or SMTP specific options '
           'overwrite general IMAP and SMTP settings.',
    add_help=False
)
# Add optional arguments
argparser.add_argument(
    '--help',
    action='help',
    help='show this help message and exit'
)
# General settings
group_general = argparser.add_argument_group('general settings')
group_general.add_argument(
    '-s', '--separator',
    help='string which separates the time from the subject'
)
group_general.add_argument(
    '-d', '--drafts',
    help='set the IMAP drafts folder'
)
group_general.add_argument(
    '-t', '--timezone',
    help='set the timezone for dates (default: UTC)'
)
group_general.add_argument(
    '-c', '--config',
    default='~/.mail_shed.cfg',
    help='set the config file (default: %(default)s)'
)
# IMAP and SMTP settings
group_imap_smtp = argparser.add_argument_group('IMAP and SMTP settings')
group_imap_smtp.add_argument(
    '-h', '--host',
    help='set the IMAP and SMTP host'
)
group_imap_smtp.add_argument(
    '-u', '--user',
    help='set the IMAP and SMTP user'
)
group_imap_smtp.add_argument(
    '-p', '--password',
    help='set the IMAP and SMTP password'
)
# IMAP settings
group_imap = argparser.add_argument_group('IMAP settings')
group_imap.add_argument(
    '-ih', '--imap-host',
    help='set the IMAP host'
)
group_imap.add_argument(
    '-iu', '--imap-user',
    help='set the IMAP user'
)
group_imap.add_argument(
    '-ip', '--imap-password',
    help='set the IMAP password'
)
# SMTP settings
group_smtp = argparser.add_argument_group('SMTP settings')
group_smtp.add_argument(
    '-sh', '--smtp-host',
    help='set the SMTP host'
)
group_smtp.add_argument(
    '-su', '--smtp-user',
    help='set the SMTP user'
)
group_smtp.add_argument(
    '-sp', '--smtp-password',
    help='set the SMTP password'
)
# Logging
group_logging = argparser.add_argument_group('logging and output settings')
group_logging.add_argument(
    '-l', '--log-file',
    default='~/mail_shed.log',
    help='set the log file (default: %(default)s)'
)
group = group_logging.add_mutually_exclusive_group()
group.add_argument(
    '-v', '--verbose',
    action='store_true',
    default=False,
    help='be verbose'
)
group.add_argument(
    '-q', '--quiet',
    action='store_true',
    default=False,
    help='don\'t output anything'
)
# Version
argparser.add_argument(
    '--version',
    action='version',
    version='%(prog)s ' + __version__,
    help='show version information and exit'
)
# Parse the arguments
args = argparser.parse_args()
# Make Path absolute
args.config = os.path.abspath(os.path.expanduser(args.config)) if args.config else None

#==============================================================================
# Logging
#==============================================================================
import logging

log_level = logging.INFO
if args.verbose:
    log_level = logging.DEBUG
elif args.quiet:
    log_level = logging.WARNING
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename=os.path.abspath(os.path.expanduser(args.log_file)),
    filemode='a', level=log_level
)

log_handler = logging.StreamHandler()
log_handler.setLevel(log_level)
log_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

log = logging.getLogger()
log.addHandler(log_handler)

log.info('Started')

#==============================================================================
# Config file parser
#==============================================================================
from ConfigParser import SafeConfigParser as ConfigParser
from StringIO import StringIO

config = ConfigParser()
config.readfp(StringIO('''
[imap/smtp]
[imap]
[smtp]
[general]
separator=|
drafts=\\Drafts
timezone=UTC
'''))

# Read config file and WARN if it has not been loaded
if len(config.read(args.config)) == 0:
    log.warn('Config file %s was not loaded', args.config)

# Overwrite the config values with the values provided via command line
for key in ('separator', 'drafts', 'timezone'):
    if getattr(args, key, None) is not None:
        config.set('general', key, getattr(args, key))

for key in ('ĥost', 'user', 'password'):
    if getattr(args, key, None) is not None:
        config.set('imap/smtp', key, getattr(args, key))

for key in ('ĥost', 'user', 'password'):
    if getattr(args, 'imap_' + key, None) is not None:
        config.set('imap', key, getattr(args, 'imap_' + key))

for key in ('ĥost', 'user', 'password'):
    if getattr(args, 'smtp_' + key, None) is not None:
        config.set('smtp', key, getattr(args, 'smtp_' + key))

# Set general host/user/password to specific if specific is not set
for connection in ('imap', 'smtp'):
    for key in ('host', 'user', 'password'):
        if (
            config.has_option('imap/smtp', key) and
            not config.has_option(connection, key)
        ):
            config.set(connection, key, config.get('imap/smtp', key))

import sys

critical_error = False

# Exit if there are config values missing
if len(config.get('general', 'separator')) == 0:
    log.critical('the separator must not be an empty string')
    critical_error = True

if len(config.get('general', 'drafts')) == 0:
    log.critical('the drafts folder must not be an empty string')
    critical_error = True

if len(config.get('general', 'timezone')) == 0:
    log.critical('the timezone must not be an empty string')
    critical_error = True

if not config.has_option('imap', 'host'):
    log.critical('there is not imap host set')
    critical_error = True
if not config.has_option('imap', 'user'):
    log.critical('there is not imap user set')
    critical_error = True
if not config.has_option('imap', 'password'):
    log.critical('there is not imap password set')
    critical_error = True

if not config.has_option('smtp', 'host'):
    log.critical('there is not smtp host set')
    critical_error = True
if not config.has_option('smtp', 'user'):
    log.critical('there is not smtp user set')
    critical_error = True
if not config.has_option('smtp', 'password'):
    log.critical('there is not smtp password set')
    critical_error = True

if critical_error:
    sys.exit(1)

#==============================================================================
# Modified IMAP library
#
# Original by Bruno Renié
# http://bruno.im/2010/jul/29/europython-talk-python-and-imap-protocol/
#==============================================================================
import imaplib

imaplib.Commands['XLIST'] = imaplib.Commands['LIST']


class IMAP4_SSL(imaplib.IMAP4_SSL):

    def xlist(self, directory='', pattern='*'):
        name = 'XLIST'
        typ, data = self._simple_command(name, directory, pattern)
        return self._untagged_response(typ, data, name)


#==============================================================================
# Main program imports
#==============================================================================
import smtplib
import email
import re
from dateutil.parser import parse as parse_datetime
from datetime import datetime
import pytz


#==============================================================================
# Main program classes, functions, constants
#==============================================================================
class IMAPError(Exception):
    pass


def result(response):
    code, data = response
    if code != 'OK':
        raise IMAPError(code)
    return data


FOLDER_LINE_RE = re.compile(
    r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)'
)


def parse_folder_line(line):
    flags, delimiter, mailbox_name = FOLDER_LINE_RE.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return flags, delimiter, mailbox_name


DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'
MAIL_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'

#==============================================================================
# Main program
#==============================================================================
# Try timezone
try:
    TIMEZONE = pytz.timezone(config.get('general', 'timezone'))
except pytz.exceptions.UnknownTimeZoneError:
    log.critical('Timezone %s does not exist', config.get('general', 'timezone'))
    sys.exit(1)

# Connect to IMAP
try:
    imap = IMAP4_SSL(config.get('imap', 'host'))
    log.debug('Connected to IMAP host %s', config.get('imap', 'host'))
except:
    log.critical(
        'Could not connect to IMAP host %s', config.get('imap', 'host')
    )
    sys.exit(1)
try:
    imap.login(config.get('imap', 'user'), config.get('imap', 'password'))
    log.debug('Logged in on IMAP host as %s', config.get('imap', 'user'))
except:
    log.critical(
        'Could not login on IMAP host as %s', config.get('imap', 'user')
    )
    sys.exit(1)

# Connect to SMTP
try:
    smtp = smtplib.SMTP_SSL(config.get('smtp', 'host'))
    log.debug('Connected to SMTP host %s', config.get('smtp', 'host'))
except:
    log.critical(
        'Could not connect to SMTP host %s', config.get('smtp', 'host')
    )
    sys.exit(1)
try:
    smtp.login(config.get('smtp', 'user'), config.get('smtp', 'password'))
    log.debug('Logged in on SMTP host as %s', config.get('smtp', 'user'))
except:
    log.critical(
        'Could not login on SMTP host as %s', config.get('smtp', 'user')
    )
    sys.exit(1)

DRAFTS = config.get('general', 'drafts')

# Get XLIST mailbox list and optionally try LIST on fail
try:
    folders = result(imap.xlist())
except IMAPError as e:
    if DRAFTS.startswith('\\'):
        log.critical(
            'Cannot fetch XLIST but needed to get drafts folder - reason %s', e
        )
        sys.exit(1)
    try:
        folders = result(imap.list())
    except IMAPError as e:
        log.critical(
            'Cannot fetch LIST but needed to get drafts folder - reason %s', e
        )
        sys.exit(1)

# Go through folders to find the right mailbox
mailbox_selected = False
for folder in folders:
    flags, _, name = parse_folder_line(folder)
    if (DRAFTS.startswith('\\') and DRAFTS in flags.split()) or DRAFTS == name:
        try:
            result(imap.select(name))
            mailbox_selected = True
            log.debug('Selected mailbox %s', name)
            DRAFTS = name
            break
        except IMAPError:
            log.critical('Cannot select mailbox %s', name)
            sys.exit(1)

if not mailbox_selected:
    log.critical('The mailbox %s was not found on the server', DRAFTS)
    sys.exit(1)

# Get all mails from the mailbox
try:
    ids = result(imap.search(None, 'ALL'))[0].replace(' ', ',')
except IMAPError as e:
    log.critical('Could not get message ids from mailbox - reason %s', e)
    sys.exit(1)

try:
    data = result(imap.fetch(ids, '(RFC822)'))
except IMAPError as e:
    log.critical('Could not get message contents - reason %s', e)
    sys.exit(1)

SEPARATOR = config.get('general', 'separator')

for line in data:
    if not isinstance(line, tuple):
        continue
    mail = email.message_from_string(line[1])

    # Check whether we can find the separator
    if mail['subject'].find(SEPARATOR) == -1:
        log.debug('Email with subject "%s" does not contain separator', mail['subject'])
        continue

    log.debug('Email with subject "%s" contains separator', mail['subject'])

    date_is_final = False

    date_part = mail['subject'][:mail['subject'].find(SEPARATOR)].strip()
    try:
        date = datetime.strptime(date_part, DATE_FORMAT)
        date = pytz.UTC.localize(date)
        date_is_final = True
        log.debug('Date is already in UTC format: %s', date)
    except ValueError:
        try:
            date = parse_datetime(date_part, dayfirst=True)
            try:
                date = TIMEZONE.localize(date, is_dst=None)
            except AmbiguousTimeError:
                date = TIMEZONE.localize(date, is_dst=False)
                log.warn('Ambigous date for DST - no DST chosen')

            date = date.astimezone(pytz.UTC)
            log.debug('Parsed UTC date: %s', date)
        except ValueError:
            log.warn('Cannot get datetime for subject %s', mail['subject'])
            continue

    msg_id = line[0].split()[0]

    if date < datetime.now(pytz.UTC):
        # Send the mail out
        del mail['message-id']
        subject = mail['subject'][mail['subject'].find(SEPARATOR) + 1:].strip()
        del mail['subject']
        mail['subject'] = subject
        try:
            smtp.sendmail(mail['from'], mail['to'], mail.as_string())
            log.info('Sent Email "%s"', mail['subject'])
            try:
                imap.store(msg_id, '+FLAGS', '(\\Deleted)')
                log.debug('Marked draft to be deleted')
            except:
                log.warn('Could not mark draft to be deleted')
        except:
            log.warn('Could not send Email "%s"', mail['subject'])

    elif not date_is_final:
        # Write UTC date into subject
        del mail['message-id']
        subject = date.strftime(DATE_FORMAT) + ' ' + mail['subject'][mail['subject'].find(SEPARATOR):].strip()
        del mail['subject']
        mail['subject'] = subject

        email_date = '"' + datetime.strptime(
            mail['date'][:mail['date'].rfind(' ')],
            MAIL_DATE_FORMAT
        ).strftime('%d-%b-%Y %H:%M:%S') + mail['date'][mail['date'].rfind(' '):] + '"'
        try:
            result(imap.append(DRAFTS, '(\\Seen)', email_date, mail.as_string()))
            log.info('Written UTC date to Email "%s"', mail['subject'])
            imap.store(msg_id, '+FLAGS', '(\\Deleted)')
            log.debug('Marked draft to be deleted')
        except Exception as e:
            log.warn('Could now write UTC date to mail subject - %s', e)


# Delete mails from IMAP
try:
    imap.expunge()
    log.debug('Deleted marked emails')
except:
    pass
# Disconnect from IMAP
try:
    imap.close()
    log.debug('Closed IMAP directory')
except:
    pass
try:
    imap.logout()
    log.debug('Logged out from IMAP')
except Exception as e:
    log.warn('Could not log out from IMAP: %s', e)

# Disconnect from SMTP
try:
    smtp.quit()
    log.debug('SMTP quit')
except Exception as e:
    log.warn('Could quit from SMTP: %s', e)

log.info('Finished')
