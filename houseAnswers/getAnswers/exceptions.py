from rest_framework.exceptions import APIException

class providerUnavailable(APIException):
    status_code = 503
    default_detail = "Provider temporarily unavailable, try again later."
    default_code = "provider_unavailable"

class informationUnavailable(APIException):
    status_code = 401
    default_detail = "Currently there are no providers registered with requested field"
    default_code = 'information_unavailable'
