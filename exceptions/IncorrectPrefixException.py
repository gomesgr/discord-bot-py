class IncorrectPrefixException(Exception):
	"""Custom exception for when a command is typed without any prefix

	Args:
		message (str): the message in which should be sent to the console
	"""
	def __init__(self, message):
		super().__init__(message)