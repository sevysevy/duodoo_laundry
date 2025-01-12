from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login as auth_login ,authenticate
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.models import User
# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect , csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Role, UserProfile , Agency
from .forms import RoleForm, UserProfileForm , AgencyForm
from django.contrib.auth import logout


class Login(auth_views.LoginView):
    redirect_authenticated_user = True

    
    def get_success_url(self):
        
        return reverse_lazy('home') 
 
    def form_invalid(self, form):
        messages.error(self.request,'Identifiants invalide')
        return self.render_to_response(self.get_context_data(form=form))
    
   
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        
       
        auth_login(self.request, user)
        self.request.session["user_role"] = user.userprofile.role.name_code
        return HttpResponseRedirect(self.get_success_url())
        

class Logout(auth_views.LogoutView):
    redirect_authenticated_user = True

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""

        
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)
    

    def get_success_url(self):
        return reverse_lazy('login') 
    


def custom_logout(request):
    logout(request)
    return redirect('login')

# Role views
@login_required
def role_list(request):
    roles = Role.objects.all().order_by('name')
    return render(request, 'role_list.html', {'roles': roles})

@login_required
def role_detail(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    return render(request, 'role_detail.html', {'role': role})

@login_required
def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rôle créé avec succès.")
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})


@login_required
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Rôle mis à jour avec succès.")
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'role_form.html', {'form': form})


@login_required
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        messages.success(request, "Rôle supprimé avec succès.")
        return redirect('role_list')
    return render(request, 'role_confirm_delete.html', {'role': role})





@login_required
# UserProfile views
def userprofile_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'userprofil_list.html', {'profiles': profiles})


@login_required
# UserProfile views
def customer_list(request):
    profiles = UserProfile.objects.filter(role__name_code__in = ['costomer'])
    return render(request, 'userprofil_list.html', {'profiles': profiles})

@login_required
def userprofile_create(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Create the User instance
            user = User(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['firstName'],
                last_name=form.cleaned_data['lastName']
            )

            if form.cleaned_data['password'] == form.cleaned_data['password2']:
            # Set the password securely
                try:
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                except IntegrityError as e:
                    messages.error(request, "Cette adresse email est deja en cours d'utilisation")

                    return render(request, 'userprofile_form.html', {'form': form})
            else:
                messages.error(request, "Les mots de passe ne sot pas identiques.")
                return render(request, 'userprofile_form.html', {'form': form})
            
            # Save the UserProfile and link it to the User
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, "Profil utilisateur créé avec succès.")
            return redirect('userprofile_list')
    else:
        form = UserProfileForm()

    return render(request, 'userprofile_form.html', {'form': form})


@login_required
def userprofile_update(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update the associated User instance
            profile.user.first_name = form.cleaned_data['firstName']
            profile.user.last_name = form.cleaned_data['lastName']
            profile.user.email = form.cleaned_data['email']
            profile.user.save()
            
            # Save the UserProfile instance
            form.save()
            messages.success(request, "Profil utilisateur mis à jour avec succès.")
            return redirect('userprofile_list')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'userprofile_form.html', {'form': form})

def userprofile_delete(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    user = profile.user
    if request.method == 'POST':
        profile.delete()

        if user:
            user.delete()

        messages.success(request, "Profil utilisateur supprimé avec succès.")
        return redirect('userprofile_list')
    return render(request, 'userprofile_confirm_delete.html', {'profile': profile})

def userprofile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'userprofil_detail.html', {'profile': profile})




def create_user(request):

    if request.method == "POST":
        lastName = request.POST.get('lastName')
        firstName = request.POST.get('firstName')
        phone = request.POST.get('phone')
        role_id = request.POST.get('role')
        email  = request.POST.get('email')
        password = request.POST.get('password')

        role = ""

        try:
            role = Role.objects.get(id = role_id)

            user = User(email = email , first_name=firstName , last_name=lastName , username = email )
            user.set_password(password) 
            user.save()

            userProfile = UserProfile(user = user , firstName = firstName , lastName = lastName , 
                                      fullName = firstName + " " + lastName , email = email , phone = phone , role = role , status = "active" )

            userProfile.save()
            context = {"id":userProfile.id}

            messages.success(request, "Utilisateur créé avec succès.")
            return redirect('userprofile_list') 
        except Exception as e :
            raise Exception(e)
        
    roles = Role.objects.all().order_by('name')
    context = {"roles":roles}
    return render(request, "create_user.html", context)



@csrf_exempt
def create_super_user(request):

    if request.method == "POST":
        print(request.POST)
        lastName = request.POST.get('lastName')
        firstName = request.POST.get('firstName')
        phone = request.POST.get('phone')
        email  = request.POST.get('email')
        password = request.POST.get('password')

        role = ""

        try:
            
            role = Role.objects.get(name_code = "admin")

            user = User(email = email , first_name=firstName , last_name=lastName , username = email , is_staff = True ,  is_superuser = True )
            user.set_password(password) 
            user.save()

            userProfile = UserProfile(user = user , firstName = firstName , lastName = lastName , fullName = firstName + " " + lastName , email = email , phone = phone ,  role = role , status = "active" )

            userProfile.save()
            context = {"id":userProfile.id}
            return JsonResponse(context)
        except Exception as e :
            raise Exception(e)
        
        
    context = {}
    return render(request, "users/management/create-user.html", context)



# views
@login_required
def agency_list(request):
    agencies = Agency.objects.all()
    return render(request, 'agency_list.html', {'agencies': agencies})

@login_required
def agency_create(request):
    if request.method == 'POST':
        form = AgencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agence créée avec succès.")
            return redirect('agency_list')
    else:
        form = AgencyForm()
    return render(request, 'agency_form.html', {'form': form})

@login_required
def agency_update(request, pk):
    agency = get_object_or_404(Agency, pk=pk)
    if request.method == 'POST':
        form = AgencyForm(request.POST, instance=agency)
        if form.is_valid():
            form.save()
            messages.success(request, "Agence mise à jour avec succès.")
            return redirect('agency_list')
    else:
        form = AgencyForm(instance=agency)
    return render(request, 'agency_form.html', {'form': form})

def agency_delete(request, pk):
    agency = get_object_or_404(Agency, pk=pk)
    if request.method == 'POST':
        agency.delete()
        messages.success(request, "Agence supprimée avec succès.")
        return redirect('agency_list')
    return render(request, 'agency_confirm_delete.html', {'agency': agency})
