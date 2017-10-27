from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required
# ----- Login and Registration ---------------

def index(request):
    context = {
        'users': User.objects.all(),
        }
    return render(request,'myapp/index.html', context)

def register(request):
    result = User.objects.validate_reg(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/')

def login(request):
    result = User.objects.login_val(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/friends')



# -----Friends/User ----------------------

def friends_page(request):
    try:
        user_id = request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'loggedin': User.objects.get(id=user_id),
        'friends': Friendship.objects.all(),
        'users': User.objects.exclude(id=user_id)
        }
    return render(request, 'myapp/friends.html', context)

def user_page(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'myapp/user.html', context)


def change_friends(request, operation, id):
    f1 = User.objects.get(id=request.session['user_id'])
    f1.save()

    f2 = User.objects.get(id=id)
    f2.save()

    if operation == 'add':
        Friendship.objects.create(
                from_friend = f1,
                to_friend = f2
            )
        return redirect("/friends")
    elif operation == 'remove':
        friend = Friendship.objects.get(id=id)
        friend.delete()
        return redirect("/friends")


# ------Logout ----------------------------

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')