def check_user_role(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                request.is_admin = True
            else:
                request.is_admin = False
        response = get_response(request)
        return response
    return middleware
