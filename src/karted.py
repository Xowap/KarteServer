# -*- encoding: utf-8 -*-

from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
import json

import auth
from auth import check_auth
import misc

KarteErrors = {
	'BadAttr': (101, 'Bad Attribute'),
	'Unexpected': (102, 'Unexpected Message'),
	'UnknownAction': (103, 'Unknown Action'),
	'Forbidden': (104, 'Forbidden Action'),
	'VerMis': (201, 'Version Mismatch'),
	'OutOfSeq': (202, 'Bad Sequence Number'),
}

KarteErrorsMap = {}
for name, value in KarteErrors.items():
	KarteErrorsMap[value[0]] = (name, value[1])

DEBUG = True

class JsonReceiver(LineReceiver, object):
	delimiter = '\n'

	def jsonReceived(self, json):
		print json

	def lineReceived(self, line):
		try:
			if DEBUG:
				print "received: ", json.loads(line)

			self.jsonReceived(json.loads(line))
		except ValueError:
			pass

	def sendJson(self, data):
		if DEBUG:
			print "sent: ", json.dumps(data)

		return self.sendLine(json.dumps(data))

class KarteProtocol(JsonReceiver):
	VERSION = 1

	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

		self.operator_id = None
		self.checkout_id = None
		self.init_done = False
		self.seq = 0
		self.auth = auth.AuthManager(None)

		self.actions = {
			'debit': self.doDebit,
			'credit': self.doCredit,
			'auth-checkout': self.doAuthCheckout,
		}

	def getOperatorId(self):
		return self.operator_id

	def getCheckoutId(self):
		return self.checkout_id

	def getInitDone(self):
		return self.init_done

	def getAuth(self):
		return self.auth

	def sendError(self, name, seq):
		msg = {
			'action': 'error',
			'code': KarteErrors[name][0],
			'name': KarteErrors[name][1],
			'seq': seq
		}
		self.sendJson(msg)

	def jsonReceived(self, json):
		try:
			seq = json.get('seq', None)
			action = json["action"]

			# Sequence number control
			self.seq += 1

			if seq != self.seq:
				self.sendError('OutOfSeq', seq)
				self.stopProducing()
				return

			# Initialize communication
			if action == "init":
				if self.init_done:
					self.sendError('Unexpected', seq)
					return

				if self.VERSION != json['version']:
					self.sendError('VerMis', seq)
					self.stopProducing()
				else:
					self.init_done = True

			else:
				if action in self.actions:
					self.actions[action](seq, json)
				else:
					self.sendError('UnknownAction')

		except (KeyError,TypeError,ValueError), ex:
			self.sendError('BadAttr', seq)

			if DEBUG:
				import traceback
				traceback.print_exc()

	@check_auth([])
	def doAuthCheckout(self, seq, json):
		if self.checkout_id != None:
			self.sendError('Unexpected', seq)
			return

		msg = {
			'action': 'result',
			'asked': 'auth-checkout',
			'seq': seq,
		}

		checkout_id = int(json["checkout_id"])

		# TODO get the correct x509 certificate
		if self.auth.authCheckout(checkout_id, None):
			msg['allowed'] = True
			self.checkout_id = checkout_id
		else:
			msg['allowed'] = False

		self.sendJson(msg)

	def doAuthOperator(self, seq, json):
		pass

	@check_auth(['debit'])
	def doDebit(self, seq, json):
		self.sendJson(['coucou'])

	@check_auth(['credit'])
	def doCredit(self, seq, json):
		pass

	# Product Management
	def doProductFetch(self, seq, json):
		pass

	def doProductUpdate(self, seq, json):
		pass

	def doProductDelete(self, seq, json):
		pass

	def doProductAdd(self, seq, json):
		pass

	# Checkout Management
	def doCheckoutFetch(self, seq, json):
		pass

	def doCheckoutUpdate(self, seq, json):
		pass

	def doCheckoutDelete(self, seq, json):
		pass

	def doCheckoutAdd(self, seq, json):
		pass

	# Role Management
	def doRoleFetch(self, seq, json):
		pass

	def doRoleUpdate(self, seq, json):
		pass

	def doRoleDelete(self, seq, json):
		pass

	def doRoleAdd(self, seq, json):
		pass

	# Tl1 Domains Management
	def doTl1DomainFetch(self, seq, json):
		pass

	def doTl1DomainUpdate(self, seq, json):
		pass

	def doTl1DomainDelete(self, seq, json):
		pass

	def doTl1DomainAdd(self, seq, json):
		pass

	# Tl1 Promotion Management
	def doTl1PromotionFetch(self, seq, json):
		pass

	def doTl1PromotionUpdate(self, seq, json):
		pass

	def doTl1PromotionDelete(self, seq, json):
		pass

	def doTl1PromotionAdd(self, seq, json):
		pass

	# User Management
	def doUserFetch(self, seq, json):
		pass

	def doUserUpdate(self, seq, json):
		pass

	def doUserDelete(self, seq, json):
		pass

	def doUserAdd(self, seq, json):
		pass

class KarteFactory(Factory):
	protocol = KarteProtocol

if __name__ == '__main__':
	factory = Factory()
	factory.protocol = Echo
	reactor.listenSSL(8000, factory,
		ssl.DefaultOpenSSLContextFactory(
		'cert/ssl.key', 'cert/ssl.pem', ssl.SSL.TLSv1_METHOD
	))
	reactor.run()
