# vim: syn=python :
import karted
from twisted.application import internet, service
from twisted.internet import ssl

port = 8000
#port = 9245
factory = karted.KarteFactory()

application = service.Application('karted')

#srv = internet.SSLServer(port, factory, ssl.DefaultOpenSSLContextFactory(
#	'cert/ssl.key',
#	'cert/ssl.pem',
#	ssl.SSL.TLSv1_METHOD
#))
srv = internet.TCPServer(8000, factory)
srv.setServiceParent(application)
