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

def _build_response(response, data_type=None, payload=None, info=None):

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


def _malformed_request(error):

	"""Creates a response for a malformed API request."""

	payload = MALFORMED_REQUESTS[error]

	errRes = _build_response('malformed-request', payload=payload)

	return {'success': False, 'err_response': errRes}


def _check_request(request):

	"""Checks for problems with the request."""

	# Checks the correct request fields are present.
	if all(field in request for field in REQUEST_FIELDS):

		# Checks the request type is permitted.
		if (request['action'] in REQUESTS):
			return {'success': True, 'result': request}

		else:
			return _malformed_request('TYPE')

	else:
		return _malformed_request('FIELDS')


def response(request, success, payload=None, info=None):

	"""Creates a response from an API request."""

	action = request['action']

	if success:
		response_type = REQUESTS[action]['success']
	else:
		response_type = REQUESTS[action]['failure']

	return _build_response(response_type, request['data_type'], payload, info)


def decode_request(request):

	"""Decodes the JSON in an API request."""

	try:
		api_request = json.loads(request)
	except json.JSONDecodeError:
		return _malformed_request('JSON')

	return _check_request(api_request)
