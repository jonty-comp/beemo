# omg global variables omg

def init():
	# defines whether an audio thread is allowed to start loading content or not.
	# if it wants to but available is false, it will keep checking until it can!
	global _available
	_available = True