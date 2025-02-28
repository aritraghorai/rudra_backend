from django.shortcuts import redirect

class AdminLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith('/admins/') and not request.path == '/admins/login/':
            if not request.user.is_authenticated or not request.user.is_staff:
                print('hai')
                return redirect('/admins/login/')  
                
        return response
