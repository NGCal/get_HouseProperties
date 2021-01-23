from rest_framework.exceptions import APIException

class providerUnavailable(APIException):
    status_code = 503
    default_detail = "Provider temporarily unavailable, try again later."
    default_code = "provider_unavailable"

class informationUnavailable(APIException):
    status_code = 401
    default_detail = "Currently there are no providers registered with requested field"
    default_code = 'information_unavailable'

class providerclassUnavailable(APIException):
    status_code = 422
    default_detail = "Provider class not available"
    default_code = 'class_unavailable'

class structureChangedAPI(APIException):
    status_code = 422
    default_detail = "The structure of the information sent by the provider changed"
    default_code = 'structure_changed'

class parametersValidationFailed(APIException):
    status_code = 400
    default_detail = "Parameters validation failed or requested key_phrase is not available"
    default_code = 'bad_parameters'

