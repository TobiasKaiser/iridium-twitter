#!/usr/bin/env python
import optparse

class IridiumMobileIFace:
	def __init__(self):
		pass

	def main(self):
		op=optparse.OptionParser()
		op.add_option("--fetch", help="Fetch messages from satellite network", action="store_true")
		op.add_option("--mail", help="Send email from file", action="append")
		op.add_option("--twitter-status", help="Update twitter status", action="append")
		op.add_option("--twitter-message", help="Send twitter private message", nargs=2, action="append", metavar="USER MESSAGE")
		op.add_option("--reg-send-auth", help="Register sending authorization", nargs=2, action="append", metavar="TOKEN NBYTES")
		op.add_option("-s", "--serial-port", help="Set serial port", action="store")
		(options, arg)=op.parse_args()
		print options, arg


if __name__=="__main__":
	IridiumMobileIFace().main()