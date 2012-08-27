MailShed
========

Simple python script which monitors your IMAP draft folder for scheduled emails.

To install create a ``schedule.cfg`` besides ``schedule.py`` and populate with at least::

    [smtp]
    user=username@googlemail.com
    pass=yourpassword

    [imap]
    user=username@googlemail.com
    pass=yourpassword

Then run::

    ./schedule.py