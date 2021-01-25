def open_access_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        # response["Allow"] = "GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS"
        return response
    return middleware
