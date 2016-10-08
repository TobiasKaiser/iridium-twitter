#!/usr/bin/python
import os, sys
import ConfigParser
import twitter
import email
import pysmile
import subprocress
import sqlite3

class IridiumTwitterGateway:
	def __init__(self):
		self.config=None

	def init_twitter_api(self):
		return twitter.Api(
			consumer_key=self.config.get("twitter_api", "consumer_key"),
			consumer_secret=self.config.get("twitter_api", "consumer_secret"),
			access_token_key=self.config.get("twitter_api", "access_token_key"),
			access_token_secret=self.config.get("twitter_api", "access_token_secret"),
				input_encoding="utf-8"
		)

	def tw_upd(self, message):
		status=self.twitter.PostUpdate(message)
		#print "%s just posted: %s" % (status.user.name, status.text)

	def tw_pm(self, user, message):
		status=self.twitter.PostDirectMessage(message, user)

	def sendmail(self, msg):
		p = subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
		p.communicate(msg)


	def rtoken(self, token, nbytes):
		



	def process_sbd_message(self, msg):
		#msg=msg[:140] # truncate message if too long
		#print msg
		#status=self.twitter.PostUpdate(msg)
		#print "%s just posted: %s" % (status.user.name, status.text)
		obj=pysmile.decode(msg)
		for command in obj:
			command, args=obj[0], obj[1:]
			if command=="tw_upd":
				self.tw_upd(args[0])
			elif command=="tw_pm":
				self.tw_pm(args[0], args[1])
			elif command=="sendmail":
				self.sendmail(args[0])
			elif command=="rtoken":
				self.rtoken(args[0], args[1])
			else:
				raise Exception("Unknown command encountered in message")
	def action_recv(self):
		print "Processing email..."
		msg=email.message_from_file(sys.stdin)
		if msg.get("To")!=self.config.get("sbd", "local_email"):
			print "To not matching"
			return
		if msg.get("From")!="sbdservice@sbd.iridium.com":
			print "From not matching"
			return
		if not msg.get("Subject").startswith("SBD Msg From Unit"):
			print "Subject not matching"
			return

		for part in msg.get_payload():
			if part.get("Content-Disposition").startswith("attachment;") and part.get_content_type().startswith("application/"):
				print "Found twittermessage"
				
				self.process_sbd_message(part.get_payload(decode=True))
				break
		else:
			print "No twitter message found"
			
	def main(self):
		self.config=ConfigParser.ConfigParser()
		if len(sys.argv)!=3:
			print "Usage: %s CONFIG_FILE recv"
			sys.exit(1)
		config_filename=sys.argv[1]
		action=sys.argv[2]
		self.config.read(config_filename)

		self.twitter=self.init_twitter_api()
		self.db = sqlite3.connect(self.config.get("db", "filename"))

		if action=="recv":
			self.action_recv()
		else:
			raise Exception("Unknown action request")

if __name__=="__main__":
	IridiumTwitterGateway().main()