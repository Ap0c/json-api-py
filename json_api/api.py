# ----- Imports ----- #

import json


# ----- Setup ----- #

# The request types and their response messages.
REQUESTS = {
	'create': {
		'success': 'created',
		'failure': 'create_fail'
	},
	'retrieve': {
		'success': 'retrieved',
		'failure': 'retrieve_fail'
	},
	'update': {
		'success': 'updated',
		'failure': 'update_fail'
	},
	'delete': {
		'success': 'deleted',
		'failure': 'delete_fail'
	}
}

# The fields that appear in a request.
REQUEST_FIELDS = ['action', 'data_type', 'payload', 'message_info']

# The error messages corresponding to failed requests.
MALFORMED_REQUESTS = {
	'JSON': 'JSON malformed.',
	'TYPE': 'Invalid request type.',
	'FIELDS': 'Invalid request fields.'
}


# ----- Internal Functions ----- #

def _buildResponse(response, data_type=None, payload=None, info=None):

	"""Creates an API response of the correct format."""

	message = {
		'response': response,
		'data_type': data_type,
		'payload': payload,
		'message_info': info
	}

	try:
		return json.dumps(message)
	except TypeError as err:
		raise Exception('Problem building response: {}'.format(err))
