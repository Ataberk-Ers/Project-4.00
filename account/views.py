from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def user_login(request):
    if request.user.is_authenticated and "next" in request.GET:
        return render(request, "account/login.html",{"error":"Yetkiniz yok."})
    
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username=username,password=password)

        if user is not None:

            login(request,user)
            nextURL = request.GET.get("next",None)
            if nextURL is None:
                return redirect("index")
            else:
                return redirect(nextURL)
        
        else:

            return render(request, "account/login.html",{"error":"Username ya da Parola yanlış"})
    else:

        return render(request,"account/login.html")

def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password != repassword:  

            return render(request,"account/register.html",
            {
                "error":"Passwords not match",
                "username": username,
                "email": email
            })
        
        if User.objects.filter(username = username).exists():

            return render(request,"account/register.html",
            {
                "error":"Username already exists",
                "username": username,
                "email": email
            })
        
        

        if User.objects.filter(email = email).exists():

            return render(request,"account/register.html",
            {
                "error":"Email already taken",
                "username": username,
                "email": email
            })
            
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect("user_login")
        
    else:
        return render(request,"account/register.html")

def user_logout(request):
    logout(request)
    return redirect("index")