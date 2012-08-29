MailShed
========

Simple python script which monitors your IMAP draft folder for scheduled emails.

To install create a ``~/.mail_shed.cfg`` (or pass path to config file via
``--config`` option) and set appropriate config options. The default values
look like this::

    # If you have (partly) the same config data for IMAP and SMTP you can set it here
    [imap/smtp]
    host=
    user=
    password=

    # This is the config only for SMTP - it overwrites settings in [imap/smtp]
    [smtp]
    host=
    user=
    password=

    # This is the config only for SMTP - it overwrites settings in [imap/smtp]
    [imap]
    host=
    user=
    password=

    # These are general options
    [general]
    # This is the string which separates your date from the real subject
    separator=|
    # In which folder should we look for mails to be sent?
    drafts=\Drafts
    # What is the timezone all dates should be in?
    timezone=Europe/Berlin


Then run::

    ./mail_shed.py

For more options and help see::

    ./mail_shed.py --help

which outputs::

    usage: mail_shed.py [--help] [-s SEPARATOR] [-d DRAFTS] [-t TIMEZONE]
                        [-c CONFIG] [-h HOST] [-u USER] [-p PASSWORD]
                        [-ih IMAP_HOST] [-iu IMAP_USER] [-ip IMAP_PASSWORD]
                        [-sh SMTP_HOST] [-su SMTP_USER] [-sp SMTP_PASSWORD]
                        [-l LOG_FILE] [-v | -q] [--version]

    Send emails from imap draft folder which should have been sent by now.

    optional arguments:
      --help                show this help message and exit
      --version             show version information and exit

    general settings:
      -s SEPARATOR, --separator SEPARATOR
                            string which separates the time from the subject
      -d DRAFTS, --drafts DRAFTS
                            set the IMAP drafts folder
      -t TIMEZONE, --timezone TIMEZONE
                            set the timezone for dates (default: UTC)
      -c CONFIG, --config CONFIG
                            set the config file (default:
                            /home/jonas/.mail_shed.cfg)

    IMAP and SMTP settings:
      -h HOST, --host HOST  set the IMAP and SMTP host
      -u USER, --user USER  set the IMAP and SMTP user
      -p PASSWORD, --password PASSWORD
                            set the IMAP and SMTP password

    IMAP settings:
      -ih IMAP_HOST, --imap-host IMAP_HOST
                            set the IMAP host
      -iu IMAP_USER, --imap-user IMAP_USER
                            set the IMAP user
      -ip IMAP_PASSWORD, --imap-password IMAP_PASSWORD
                            set the IMAP password

    SMTP settings:
      -sh SMTP_HOST, --smtp-host SMTP_HOST
                            set the SMTP host
      -su SMTP_USER, --smtp-user SMTP_USER
                            set the SMTP user
      -sp SMTP_PASSWORD, --smtp-password SMTP_PASSWORD
                            set the SMTP password

    logging and output settings:
      -l LOG_FILE, --log-file LOG_FILE
                            set the log file (default: /home/jonas/mail_shed.log)
      -v, --verbose         be verbose
      -q, --quiet           don't output anything

    Options given via command line are preferred over options set in config file.
    IMAP or SMTP specific options overwrite general IMAP and SMTP settings.
