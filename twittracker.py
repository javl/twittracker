#!/usr/bin/env python

import tweepy, datetime, json, commands

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

followers_list = []

for follower in tweepy.Cursor(api.followers).items():
	followers_list.append([follower.name, follower.screen_name])

#write contacts to file
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H:%M")

status, old_file = commands.getstatusoutput('ls *.json -t | head -n 1')

try:
    with open(timestamp+'.json','wb') as f:
        f.write(json.dumps(followers_list))
except IOError:
    print "Couldn't write contacts to file"
    sys.exit(1)
print "Done writing new contacts (%i)" % len(followers_list)

if old_file != '':
	print "Compare to %s" % old_file
	data_old = json.loads(open(old_file).read());

	same = True
	for x in data_old:
		if x not in followers_list:
			same = False
			print "Missing!"
			print x

	for x in followers_list:
		if x not in data_old:
			same = False
			print "NEW!"
			print x

	if same:
		print "Nothing changed."
