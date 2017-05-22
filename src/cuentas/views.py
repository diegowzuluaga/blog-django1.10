from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout
	)
from django.shortcuts import render, redirect

from .forms import UserLoginForm	, UserRegForm

# Create your views here.
def login_view(request):
	next = request.GET.get("next")
	titulo = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		usuario = form.cleaned_data.get("usuario")
		password = form.cleaned_data.get("password")
		user = authenticate(username=usuario, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")
	return render(request, "form.html", {"form": form, "titulo": titulo})

def register_view(request):
	titulo = "Registrarse"
	form = UserRegForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		return redirect("/")
	context = {
		"titulo": titulo,
		"form": form,
	}
	return render(request, "form.html", context)

def logout_view(request):
	logout(request)
	return redirect("/")

# Create your views here.
