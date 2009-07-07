#!/usr/bin/python
# PythonProwlScript, to communicate with the Prowl server.
# Copyright 2009 Camron Flanders
#
# Ported from Zachary West's prowl.pl script
#
# This requires running Prowl on your device.
# See the Prowl website <http://prowl.weks.net>
# 
# also requires httplib2

import sys
import httplib2
import urllib
import optparse

BASE_URL = "https://prowl.weks.net/api/add_notification.php?"
USER_AGENT = "PythonProwlScript/1.0"

USERNAME = None
PASSWORD = None

def password_from_file(filename):
    """
    Extracts a password from a file.

    """
    if not isinstance(filename, (unicode, str)):
        return False

    f = open(filename)
    #get password, needs to be only thing on first line
    password = f.readlines()[0].strip('\n')
    f.close()

    return password

def post_notification(application, event="", description=""):
    """
    Sends a notification to the Prowl server, which is then forwarded to your device running the Prowl application.
    For more assistance, visit the Prowl website at <http://prowl.weks.net>.

    """
    kwargs = {'application':application, 
              'event':event, 
              'description':description,}

    if not PASSWORD:
        print "Password, or password file, is required."
        return

    for k,v in kwargs.iteritems():
        if not v:
            print "'%s' text is required." % k.title()
            return

    H = httplib2.Http(timeout=15)
    H.force_exception_to_status_code = True
    H.add_credentials(USERNAME, PASSWORD)

    rsp, content = H.request(BASE_URL + urllib.urlencode(kwargs))

    if not rsp.status == 200:
        log.error('status code returned: %s', response.status)
        log.error('content recieved: %s' % content)
        return False

    if rsp.status == 200:
        print "Notification successfully posted.\n"
    elif rsp.status == 401:
        print "Notification not posted: incorrect username or password.\n"
    else:
        print "Notification not posted: %s" % rsp.status

if __name__ == "__main__":
    usage = "prowl.py [options] event_text"

    parser = optparse.OptionParser(usage)

    parser.add_option("-u", "--username", metavar="username", help="Your Prowl username.")
    parser.add_option("-p", "--password", metavar="password", help="Your Prowl password.")
    parser.add_option("-f", "--passwordfile", metavar="file_path", help="A file containing your Prowl password.")
    parser.add_option("-a", "--application", metavar="text", help="The name of the application.")
    parser.add_option("-e", "--event", metavar="text", help="The name of the event.")
    parser.add_option("-n", "--notification", metavar="text", help="The text of the notification.")

    opts, args = parser.parse_args(sys.argv)

    if not opts.username:
        print "Username, password, and event information are required."
        print "use -h or --help for more information."
    else:
        USERNAME = opts.username
        PASSWORD = password_from_file(opts.passwordfile) if opts.passwordfile else opts.password

        post_notification(opts.application, opts.event, opts.notification)
