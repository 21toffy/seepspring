from celery import shared_task
from celery.utils.log import get_task_logger
# from seepspring.celery import app



logger = get_task_logger(__name__)


@shared_task
def sample_task():
    print(122222222222222222222222222222222222222222222)
    logger.info("The sample task just ran.")



# @app.task(name="update_defaulters_new_balance", bind=True)

@shared_task
def update_defaulters_new_balance():
    import datetime
    from loan.models import UserLoan
    from django.utils import timezone
    todays_date = datetime.date.today()
    defaulted_loans = UserLoan.objects.filter(active=True, paid=False, loan_due_date__lt=todays_date)
    print(defaulted_loans)
    for dl in defaulted_loans:
        try:
            loan_days = dl.loan_level.days_tenure
            interest_percentage = dl.interest.aggregated_interest
            amount_per_day = (interest_percentage*dl.amount_left)/100
            new = amount_per_day/loan_days
            dl.accumulated_amount = dl.accumulated_amount + new
            dl.last_accumulate_date=timezone.now().date()
            dl.save()

        except Exception as e:
            pass
    return True

