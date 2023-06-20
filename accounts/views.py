from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    elif request.method == 'POST':
        data = request.POST
        email = data['email']
        password = data['password']
        try:
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                status = 'authenticated'
                
            else:
                status = 'failed'
                response = {
                    'status': status
                }
                return JsonResponse(response)
        except:
            status = 'failed'
        response = {
            'status': status
        }
        return JsonResponse(response)
    else:
        title = "Login | Dominique's Dishes"
        context = {
            'title': title,
        }
        return render(request, 'login.html', context)
    