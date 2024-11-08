from django.utils import timezone
from .models import SaleSession

def has_valid_sale_session():
    today = timezone.now().date()
    has_valid_session = SaleSession.objects.filter(
        status='open', 
        start_time__date=today
    ).exists()

    return has_valid_session