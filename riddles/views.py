from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from .models import Info, Riddles, Solution, Terminate, Start

from .forms import SolutionForm
from django.template.context_processors import csrf

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('loggedin')
	else: 
		allusers= User.objects.order_by('-foo__score')
		users=[]
		for x in allusers:
			if not x.is_superuser:
				users.append(x)
		return render(request, 'index.html', {'users': users})


def login_view(request):
	try:
		username =request.POST['username']
		password= request.POST['password']
		user = authenticate(username=username, password=password)
	except KeyError:
		return render(request, 'index.html',{'login_message' : 'Fill in all fields',}) 
	if user is not None:
		if user.is_active:
			login(request,user)
			return redirect('loggedin')
		else:
			return render(request, 'index.html',{'login_message' : 'The user has been removed',})
	else:
		return render(request, 'index.html',{'login_message' : 'Enter Correct Details',})

@login_required
def loggedin(request):
	if request.user.is_superuser:
		allusers= User.objects.all()
		allsubmits= Solution.objects.all()
		dicb ={}
		for x in allusers:
			if not x.is_superuser:
				name= x.foo.team_name +' - '+ x.foo.member1
				dicb[name]=Solution.objects.filter(user__id=x.id)

		return render(request, 'admin.html', {'dicb': dicb})
	else:
		riddles = Riddles.objects.all()
		solution= Solution.objects.filter(user= request.user)
		k=[]
		for sol in solution:
			k.append(sol.riddle.id)
		for x in k:
			riddles= riddles.exclude(id=x)

		c={}
		c['riddles']=riddles
		if not len(Terminate.objects.all()) and len(Start.objects.all()):
			return render(request, 'team.html', c)
		elif not len(Start.objects.all()):
			return render(request, 'eventwillstart.html', {})
		else:
			return render(request, 'eventover.html', {})

#view to display previous submissions
@login_required
def submissions(request):
	submits= Solution.objects.filter(user= request.user)
	return render(request, 'submissions.html', {'submits': submits})


@login_required
def submit(request, riddle_id):
	temp= get_object_or_404(Riddles, pk=riddle_id)
	if request.POST:
		form= SolutionForm(request.POST, request.FILES)
		if form.is_valid():
			sol=form.save(commit=False)
			sol.riddle= Riddles.objects.get(pk=riddle_id)
			sol.user= request.user
			sol.submitted= True
			sol.save()
			return redirect('loggedin')
	else:
		form = SolutionForm()
	x= Solution.objects.filter(user__id= request.user.id , riddle__id=riddle_id)
	y= Riddles.objects.get(pk=riddle_id)
	args={}
	args.update(csrf(request))
	args['form']= form
	args['riddle_id']=riddle_id
	args['riddle']=y
	if len(x)==0 :
		args['submitted']= False
	else:
		args['submitted']= True

	if not len(Terminate.objects.all()) and len(Start.objects.all()):
		return render(request, 'sol_form.html', args)
	else:
		return redirect('loggedin')


@login_required	
def logout_view(request):
	logout(request)
	return redirect('index')

@login_required
def correct(request, user_id, riddle_id):
	if request.user.is_superuser:
		solution= Solution.objects.filter(riddle=riddle_id, user= user_id)
		print("called")
		for sol in solution:
			if sol.correct is not True:
				user= User.objects.get(pk= user_id)
				user.foo.score+=4
			sol.correct = True
			sol.save()
			user.foo.save()
		return HttpResponse('')

@login_required
def wrong(request, user_id, riddle_id):
	if request.user.is_superuser:
		solution= Solution.objects.filter(riddle=riddle_id, user= user_id)
		for sol in solution:
			sol.correct = False
			sol.save()
		user= User.objects.get(pk= user_id)
		user.foo.save()
		return redirect('loggedin')
'''
@login_required
def map(request):
	return render(request, 'map.html', {} )
'''
@login_required
def standings(request):
	allusers= User.objects.order_by('-foo__score')
	users=[]
	for x in allusers:
		if not x.is_superuser:
			users.append(x)
	if request.user.is_superuser:
		return render(request, 'standingsadmin.html', {'users': users})
	else:
		return render(request, 'standings.html', {'users': users})

@login_required
def shutdown(request):
	if request.user.is_superuser:
		return render(request, "sure.html", {})

@login_required
def sureshutdown(request):
	if request.user.is_superuser:
		x=Terminate()
		x.save()
	return redirect('loggedin')


@login_required
def start(request):
	if request.user.is_superuser:
		if len(Start.objects.all()):			
			return redirect('loggedin')
		else:
			return render(request, "surestart.html", {})

@login_required
def surestart(request):
	if request.user.is_superuser:
		x=Start()
		x.save()
	return redirect('loggedin')



