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

# The fields that appear in a response.
RESPONSE_FIELDS = ['response', 'data_type', 'payload', 'message_info']

# The error messages corresponding to failed requests.
MALFORMED_REQUESTS = {
	'JSON': 'JSON malformed.',
	'TYPE': 'Invalid request type.',
	'FIELDS': 'Invalid request fields.'
}

# The error messages corresponding to problematic responses.
MALFORMED_RESPONSES = {
	'JSON': 'JSON malformed.',
	'TYPE': 'Invalid response type.',
	'FIELDS': 'Invalid response fields.'
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

	"""Checks for problems with a received request."""

	# Checks the correct request fields are present.
	if all(field in request for field in REQUEST_FIELDS):

		# Checks the request type is permitted.
		if (request['action'] in REQUESTS):
			return {'success': True, 'result': request}

		else:
			return _malformed_request('TYPE')

	else:
		return _malformed_request('FIELDS')


def _check_response(request, response):

	"""Checks for problems with a received response."""

	# Checks the correct response fields are present.
	if all(field in response for field in RESPONSE_FIELDS):

		action = request['action']
		allowed_responses = list(REQUESTS[action].values()) + ['malformed-request']

		# Checks the response type is permitted.
		if (response['response'] in allowed_responses):
			return {'success': True, 'result': request}

		else:
			return {'success': False, 'error': MALFORMED_RESPONSES['TYPE']}

	else:
		return {'success': False, 'error': MALFORMED_RESPONSES['FEILDS']}


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


def request(action, data_type=None, payload=None, info=None):

	"""Creates a JSON request."""

	if action in REQUESTS:

		message = {
			'action': action,
			'data_type': data_type,
			'payload': payload,
			'message_info': info
		}

		try:
			return message, json.dumps(message)
		except TypeError as err:
			raise Exception('Problem building request: {}'.format(err))

	else:
		raise Exception('Request verb not permitted: {}'.format(action))


def decode_response(request, response):

	"""Decodes the JSON in an API response."""

	try:
		api_response = json.loads(response)
	except json.JSONDecodeError:
		return {'success': False, 'error': MALFORMED_RESPONSES['JSON']}

	return _check_response(request, api_response)
