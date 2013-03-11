class GrowlError(Exception):
	pass

class ParseError(GrowlError):
	errorcode = 500
	errordesc = 'Error parsing the message'

class AuthError(GrowlError):
	errorcode = 400
	errordesc = 'Error with authorization'



class UnsupportedError(GrowlError):
	errorcode = 500
	errordesc = 'Currently unsupported by gntp.py'



class NetworkError(GrowlError):
	errorcode = 500
	errordesc = "Error connecting to growl server"

