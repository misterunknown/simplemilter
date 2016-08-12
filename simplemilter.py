#!/usr/bin/env python

import Milter
from Milter.utils import parse_addr
import os
import re

class simplemilter(Milter.Base):

	def __init__(self):
		self.id = Milter.uniqueID()

	def envfrom(self, mailfrom, *str):
		f = parse_addr(mailfrom)
		if len(f) > 1:
			self.env_from_domain = f[1]
			print '{} Registered env_from_domain: {}'.format(self.id, f[1])
			return Milter.CONTINUE
		else:
			return Milter.ACCEPT

	def header(self, key, value):
		if key == 'DKIM-Signature':
			d = re.search(' d=([^\s;]+)', value)
			if d:
				print '{} DKIM-Match found: {}'.format(self.id, d.group(1))
				if self.env_from_domain != d.group(1):
					return Milter.REJECT
				else:
					return Milter.ACCEPT
			else:
				return Milter.REJECT
		else:
			return Milter.CONTINUE
			
def main():
	socketname = "/var/spool/postfix/simplemilter/simplemilter"
	timeout = 600
	Milter.factory = simplemilter
	Milter.runmilter("simplemilter", socketname, timeout)

if __name__ == "__main__":
	main()
