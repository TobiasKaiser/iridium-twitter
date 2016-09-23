#!/usr/bin/python
import os, sys
import ConfigParser
import twitter

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

	def action_recv(self):
		status=self.twitter.PostUpdate("How is it going?")
		print "%s just posted: %s" % (status.user.name, status.text)

	def main(self):
		self.config=ConfigParser.ConfigParser()
		if len(sys.argv)!=3:
			print "Usage: %s CONFIG_FILE recv"
			sys.exit(1)
		config_filename=sys.argv[1]
		action=sys.argv[2]
		self.config.read(config_filename)

		self.twitter=self.init_twitter_api()

		if action=="recv":
			self.action_recv()
		else:
			raise Exception("Unknown action request")

if __name__=="__main__":
	IridiumTwitterGateway().main()