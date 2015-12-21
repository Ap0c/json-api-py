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
