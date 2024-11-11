from django.shortcuts import render, redirect , get_object_or_404
from django.utils import timezone
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from UserManagement.models import Agency
from .models import SaleSession

# Create your views here.

@login_required
def home(request):
    
    context = {
    }
    return render(request, 'home.html', context)



@login_required
def sale_session_list(request):
    # Get all sale sessions, ordered by start time (most recent first)
    sessions = SaleSession.objects.order_by('-start_time')
    
    # Pagination: Show 10 sessions per page
    paginator = Paginator(sessions, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sale_session_list.html', {'page_obj': page_obj})

@login_required
def open_sale_session(request):
    # Check if there’s an open session for the current user today
    today = timezone.now().date()
    existing_session = SaleSession.check_open_session() 
    agency = Agency.objects.last()

    if existing_session:
        messages.error(request, "Une session est déjà ouverte, vous devez la fermer avant de continuer.")
        return redirect('sale_session_list')  # Redirect to the session list page if a session is already open

    if agency is None:
        messages.error(request, "Vous devez configurer votre Agence.")
        return redirect('sale_session_list')  # Redirect to the session list page if a session is already open

    last_session = SaleSession.objects.filter(status='closed').order_by('-end_time').first()
    opening_fund = last_session.closing_fund if last_session else 0.00
    # Create a new session if none exists for today
    
    session = SaleSession.objects.create(user=request.user.userprofile , opening_fund=opening_fund , agency=agency)
    messages.success(request, "Nouvelle session ouverte avec succès.")
    return redirect('sale_session_list')  # Redirect to the session list page after opening a new session



def propose_closing_amount(session):
    """Calculate proposed closing amount based on funds in session."""
    print(session.added_fund)
    return session.opening_fund + session.added_fund - session.removed_fund

def close_sale_session(request, session_id):
    session = get_object_or_404(SaleSession, id=session_id, status='open')
    
    if request.method == 'POST':
        # Get the user-confirmed closing amount from the form submission
        closing_amount = request.POST.get('closing_amount')
        
        # Set the session fields and close it
        session.closing_fund = float(closing_amount)
        session.close_session()
        messages.success(request, "Session fermée avec succès.")
        return redirect('sale_session_list')

    # If it's a GET request, propose a calculated closing amount
    proposed_closing_amount = propose_closing_amount(session)
    
    return render(request, 'close_session.html', {
        'session': session,
        'proposed_closing_amount': proposed_closing_amount
    })