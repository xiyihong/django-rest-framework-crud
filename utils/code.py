class StatusCode(int):
    def __str__(self):
        if has_code(self):
            return __code_to_message[self]
        else:
            return str(unknown_error)

def has_code(code):
    return code in _code_to_message

success = StatusCode(200)
unknown_error = StatusCode(501)
internal_error = StatusCode(502)
param_missing = StatusCode(408)
param_illegal = StatusCode(409)
invalid_data = StatusCode(410)
biz_error = StatusCode(503)

_code_to_message = {
    success: 'success',
    internal_error: 'internal_error',
    param_missing: 'param_missing',
    param_illegal: 'param_illegal',
    unknown_error: 'unknown_error',
    biz_error: 'biz_error',
    invalid_data: 'invalid_data',
}