# -*- encoding: utf-8 -*-

from functools import wraps

def check_auth(actions=[], init=True):
	def wrap(f):
		@wraps(f)
		def wrapper(obj, seq, json):
			if init != obj.getInitDone():
				obj.sendError('Unexpected', seq)
				return

			#if actions == 'json':
			#	actions = [json['action']]
			#actions = [json['action']]

			#for a in actions:
			#	if not obj.getAuth().authorizeAction(a, obj.getOperatorId(), obj.getCheckoutId(), json.get('client', None)):
			#		obj.sendError('Forbidden', seq)
			#		return

			return f(obj, seq, json)
		return wrapper
	return wrap

class AuthManager(object):
	def __init__(self, db):
		self.db = db

	def authCheckout(self, checkout_id, x509):
		return True

	def authOperator(self, operator_id, card_info, password):
		return True

	def authClient(self, client_id, card_info):
		return True

	def authorizeAction(self, action, operator_id = None, checkout_id = None, client_id = None):
		return operator_id != None and checkout_id != None
