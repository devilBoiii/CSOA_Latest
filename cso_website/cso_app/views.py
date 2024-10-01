from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime,timedelta
from .models import *
from .decorators import *
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import check_password
from django.conf import settings
import requests
import random
# Create your views here.
#######recommend the following functions its for notifying the CSO before one month of validity date####

# def my_daily_task():
#     # Get today's date
#     today = datetime.now().date()  # timezone-aware
    
#     # Calculate the date 30 days from now
#     notification_date = today + timedelta(days=30)
#     # Query for CSOs whose validity date is 30 days away
#     cso_list = CSO_lists.objects.filter(cso_validity_date=notification_date)
#     # Send email notifications
#     for cso in cso_list:
#         # Construct email message
#         subject = 'License Renewal Notification'
#         message = f"Dear {cso.cso_name},\n\nYour validity date is coming up on {cso.cso_validity_date}. Please take the necessary actions by renewing it.\n Click here: http://127.0.0.1:8000/pay_fees/\n\nBest regards,\nCSOA"
#         sender = "devilboi150@gmail.com"        
#         recipient_list = [cso.cso_email]  # Assuming CSO model has an email field
        
#         # Send the email
#         send_mail(subject, message, sender, recipient_list)
        
#     print("Task ran!!!!!!!!")

# def check_and_run_task():
#     last_run_time = timezone.now() - timedelta(days=1)
#     num_iterations = 10  # Example: run the loop 10 times
#     for _ in range(num_iterations):
#         current_time = timezone.now()
#         if current_time - last_run_time >= timedelta(days=1):
#             my_daily_task()
#             last_run_time = current_time
#         time.sleep(7200)  # Sleep for 2 hrs
# # Run check_and_run_task in a separate thread or process
# import threading
# def start_task():
#     task_thread = threading.Thread(target=check_and_run_task)
#     task_thread.start()

# # Call start_task() to run check_and_run_task in a new thread
# start_task()
###Till here
def custom_404(request, exception):
    return render(request, '404.html', status=404)

####For Payment Integrations
def get_access_token():
    url = 'https://stg-sso.tech.gov.bt/oauth2/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'GuvmU_u9ssVJuoZkVwgHqjQVyXIa',
        'client_secret': 'fED2Ig2mszkv04wLawgESd1clpca'
    }
    response = requests.post(url, data=data)
    response.raise_for_status()  # Will raise an error for bad responses
    return response.json().get('access_token')


def home(request):
    current_year = datetime.now().year
    posts = post_publish.objects.all()
    context = {'current_year': current_year, 'posts':posts}
    return render(request, 'cso_app/home.html', context)

def cso_authority(request):

    return render(request, 'cso_app/about/authority.html')

def vision_mission(request):

    return render(request, 'cso_app/about/vision&mission.html')

def organogram(request):

    return render(request, 'cso_app/about/organogram.html')

#whoiswho
def composition(request):
    return render(request, 'cso_app/whoiswho/composition.html')

def authority_members(request):
    return render(request, 'cso_app/whoiswho/authority_members.html')

def cso_staff(request):
    return render(request, 'cso_app/whoiswho/cso_staff.html')

#Registered_CSOs
def pbos(request):
    pbos = CSO_lists.objects.filter(cso_type = 'PBO')
    context = {'pbos': pbos}
    return render(request, 'cso_app/registered_cso/pbos.html', context)

def mbos(request):
    mbos = CSO_lists.objects.filter(cso_type = 'MBO')
    context = {'mbos': mbos}
    return render(request, 'cso_app/registered_cso/mbos.html', context)

def home_cso_detail(request, cso_id):
    # Fetch the CSO object by its ID
    cso = get_object_or_404(CSO_lists, cso_id=cso_id)
    try:
        attachment_history = cso_attachment_and_fees.objects.get(cso_id=cso_id)
    except cso_attachment_and_fees.DoesNotExist:
        attachment_history = None    
    context = {'cso':cso, 'attachment_history':attachment_history}
    # Pass the CSO object to the template
    return render(request, 'cso_app/registered_cso/home_cso_detail.html', context)

def foreign_cso(request):
    return render(request, 'cso_app/registered_cso/foreign_cso.html')

def thematic(request):
    return render(request, 'cso_app/registered_cso/thematic.html')

#News Functions]
def news(request):
    return render(request, 'cso_app/news/news.html')

#Contact_Us Functions]
def contact_us(request):
    return render(request, 'cso_app/contact_us/contact_us.html')

#Feedback Functions]
def feedback(request):
    return render(request, 'cso_app/feedback/feedback.html')
def feedback_form(request):
    full_name = request.POST.get('fullname')
    email = request.POST.get('email')
    mobile_no = request.POST.get('mobile_no')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    feedback = FeedBackForm(
        full_name=full_name,
        email = email,
        mobile_number = mobile_no,
        subject = subject,
        message = message,
    )
    feedback.save()
    print("Reaching Here Coding can be be done baro")
    return redirect('feedback')

#downloads_links
def cso_act_2007(request):
    return render(request, 'cso_app/downloads/cso_act_2007.html')

def publications(request):
    return render(request, 'cso_app/downloads/publications.html')

def downloads_forms(request):
    return render(request, 'cso_app/downloads/download_forms.html')



@unauthenticated_user
def sign_in(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Basic validation
        if username and password:
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Successful authentication
                login(request, user)
                user_detail = SignInDetails(username=username, password=user.password, sign_in_date=timezone.now())
                user_detail.save()
                user.status = 'Active'  # Assuming user is now active
                user.save()
                return redirect('administrator')  # Redirect to a success page
            else:
                # Invalid credentials
                error_message = "Invalid username or password."
        else:
            error_message = "Both fields are required."

    return render(request, 'cso_app/sign_in/sign_in.html', {'error_message': error_message})

def sign_out(request):
    current_user = request.user
    # Update user status to 'inactive' on sign out
    if current_user.is_authenticated:
        # Fetch the SignInDetails object for the current user
        try:
            sign_in_details = SignInDetails.objects.filter(username=current_user.username).latest('sign_in_date')
            sign_in_details.sign_out_date = timezone.now()
            sign_in_details.save()
        except SignInDetails.DoesNotExist:
            print("SignInDetails for the user does not exist.")

        # Update user status to 'inactive'
        current_user.status = 'Inactive'
        current_user.save()

    # Log out the user
    logout(request)
    return redirect('home')


def feedback_table(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all()
    feedbacks = FeedBackForm.objects.all()
    context = {'role':role, 'feedbacks':feedbacks,'notifications_list':notifications_list}
    return render(request, "cso_app/administrator/feedback/feedback_table.html", context)

def pay_fees(request):
    csos = CSO_lists.objects.all()

    combined_cso_list = csos
    new_cso = CSO_lists.objects.filter(status = 'new')
    context = {'combined_cso_list': combined_cso_list, 'new_cso':new_cso}
    return render(request, 'cso_app/fees/pay_fees.html', context)

# @csrf_exempt

def validate_info(request):
    cso_id = request.GET.get('cso_id') or request.GET.get('cso_id1')
    amendment_fees = request.GET.get('amendment_fees')
    fees_payment = request.GET.get('fees_payment')
    cso = get_object_or_404(CSO_lists, cso_id=cso_id)
    days_diff = 0
    if not cso_id:
        return JsonResponse({'error': 'Invalid or missing CSO ID'}, status=400)
    request.session['cso_id'] = cso_id
    # Map user selection to corresponding fine amount
    amendment_fees_mapping = {
        'one amendment': 500,
        'two amendment': 1000,
        'three amendment': 1500,
        'four amendment': 2000,
        'five amendment': 2500,
        'whole amendment': 3000
    }
    cso_ammendment_fine = amendment_fees_mapping.get(amendment_fees, 0)
    fine = []
    try:
        cso = get_object_or_404(CSO_lists, cso_id=cso_id)
        validity_date = cso.cso_validity_date
        current_date = timezone.now().date()  # Use date() to get only the date part
        
        if validity_date > current_date:
            fine = 0
        else:
            difference = relativedelta(current_date, validity_date)
            months_diff = difference.years * 12 + difference.months
            days_diff = (current_date - validity_date).days  
            # Calculate days fine
            if days_diff <= 90:
                days_fine = 100 * days_diff
            else:
                days_fine = (90 * 100) + ((days_diff - 90) * 200)

            if days_diff > 180:
                late_fine = 100000
                total_fine = late_fine + days_fine
                fine.append(total_fine)
            elif days_diff >= 90:
                late_fine = 30000
                total_fine = late_fine + days_fine
                fine.append(total_fine)
            elif days_diff <= 90:
                late_fine = 10000
                total_fine = late_fine + days_fine
                fine.append(total_fine)
            else:
                return JsonResponse({'error': 'Validity Date Not Found'}, status=404)
        certificate_payment_fee = 50000 if fees_payment in ['invalid certificate', 'whole fees'] else 0
        def calculate_total_fines(fine, cso_ammendment_fine,certificate_payment_fee):
            if isinstance(fine, list):
                if len(fine) > 0:
                    total_fines = fine[0] + cso_ammendment_fine + certificate_payment_fee
                else:
                    total_fines = cso_ammendment_fine + certificate_payment_fee
            else:
                total_fines = fine + cso_ammendment_fine + certificate_payment_fee
            return total_fines
        overall_fines = calculate_total_fines(fine, cso_ammendment_fine, certificate_payment_fee)

        # Check for invalid certificate payment

        # Store data in session
        request.session['overall_fines'] = overall_fines
        request.session['cso_ammendment_fine'] = cso_ammendment_fine
        request.session['cso_name'] = cso.cso_name
        def days_fine(amount):
            if isinstance(amount, list):
                if len(amount) > 0:
                    amount = fine[0]
            else:
                amount = fine
            return amount
        fines = days_fine(fine)
        request.session['fines'] = fines
        cso_info = {
            'cso_name': cso.cso_name,
            'cso_status': cso.status,
            'days_diff':days_diff,
            'cso_application_date': cso.application_date.strftime('%Y-%m-%d'),
            'cso_ammendment_fine': cso_ammendment_fine,
            'cso_validity_date': validity_date.strftime('%Y-%m-%d'),
            'cso_registration_date': cso.cso_registered_date.strftime('%Y-%m-%d'),
            'cso_logo': cso.cso_logo.url if cso.cso_logo else '',
            'cso_contact': cso.cso_contact,
            'fine': fine,
            'overall_fines': overall_fines,
            'certificate_payment_fee': certificate_payment_fee
        }
        return JsonResponse({'cso_info': cso_info})
    except CSO_lists.DoesNotExist:
        return JsonResponse({'error': 'CSO not found'}, status=404)

    
    except CSO_lists.DoesNotExist:
        return JsonResponse({'error': 'CSO not found'}, status=404)

def pay_fees_attachment(request):
    if request.method == 'POST':
        cso_id = request.session.get('cso_id')
        if not cso_id:
            print("Could not find CSO_ID")
            return JsonResponse({'success': False, 'message': 'CSO ID not found in session.'}, status=400)
        cso = cso_attachment_and_fees.objects.create(cso_id_id=cso_id)

        try:
            cso.cso_id_id = cso_id
            cso.save()

            annual_report_file = request.FILES.get('annual_report_file')
            if annual_report_file:
                cso.annual_report = annual_report_file
                cso.save()

            audit_report_file = request.FILES.get('audit_report_file')
            if audit_report_file:
                cso.audit_report = audit_report_file
                cso.save()

            two_yrs_work_plan_file = request.FILES.get('two_yrs_work_plan_file')
            if two_yrs_work_plan_file:
                cso.two_yrs_report = two_yrs_work_plan_file
                cso.save()

            annual_general_report_file = request.FILES.get('annual_general_report_file')
            if annual_general_report_file:
                cso.annual_general_report = annual_general_report_file
                cso.save()

            request.session['payment_id'] = str(cso.payment_id)

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error saving files.'}, status=500)

        return JsonResponse({'success': True, 'payment_id': str(cso.payment_id)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


def pay_fees_form(request):
    if request.method == 'POST':
        payment_id = request.session.get('payment_id')  # Retrieve payment_id from session
        if not payment_id:
            cso_id = request.session.get('cso_id')

            full_name = request.POST.get('full_name')
            cso_name = request.session.get('cso_name')
            acct_name = request.POST.get('acct_name')
            acc_numba = request.POST.get('acc_numba')
            cid = request.POST.get('cid')
            fees_payment = request.POST.get('fees_payment')
            bank_type = request.POST.get('bank_type')
            amount = request.POST.get('amount')
            otp = request.POST.get('otp')
            acct_email = request.POST.get('acct_email')
            mobile_no = request.POST.get('mobile_no')
            jrl_number = request.POST.get('jrl_number')
            new_payment = cso_attachment_and_fees(
                cso_name=cso_name,
                bank_type=bank_type,
                account_number=acc_numba,
                user_name=full_name,
                user_email=acct_email,
                otp=otp,
                account_name=acct_name,
                user_cid=cid,
                fees_payment_type=fees_payment,
                mobile_number=mobile_no,
                amount_paid=amount,
                journal_number = jrl_number,
                cso_id_id = cso_id
            )
            new_payment.save()
            return JsonResponse({'success': True, 'message': 'Payment ID not found in session.'})

        # Retrieve the payment instance
        payment = get_object_or_404(cso_attachment_and_fees, payment_id=payment_id)

        # Update the payment instance with form data
        payment.user_name = request.POST.get('full_name')
        payment.account_number = request.POST.get('acc_numba')
        payment.amendment_type = request.POST.get('amendment_fees')
        payment.amendment_fees = request.POST.get('cso_ammendment_fine')
        payment.fees_payment_type = request.POST.get('fees_payment')
        payment.bank_type = request.POST.get('bank_type')
        payment.account_name = request.POST.get('acct_name')
        payment.otp = request.POST.get('otp')
        payment.amount_paid = request.POST.get('amount')
        payment.user_email = request.POST.get('acct_email')
        payment.mobile_number = request.POST.get('mobile_no')
        payment.late_renewal_fees = request.POST.get('fines')
        payment.user_cid = request.POST.get('cid')
        payment.overall_fines = request.session.get('overall_fines')
        payment.cso_name = request.session.get('cso_name')
        payment.journal_number = request.POST.get('jrl_number')

        # Save the updated payment instance
        payment.save()

        # Clear session data after use
        request.session.pop('payment_id', None)
        request.session.pop('overall_fines', None)
        request.session.pop('fines', None)
        request.session.pop('cso_ammendment_fine', None)
        request.session.pop('cso_name', None)

        # Redirect to a success page or render the same page with a success message
        return redirect('pay_fees')  # Change 'pay_fees' to your success URL name

    context = {
        'combined_cso_list': CSO_lists.objects.all(),  # Add your CSO list to the context
    }
    return render(request, 'cso_app/fees/pay_fees.html', context)


#Administration Side
#I need to add a decorator here cause right now this is accessible to every use
@login_required
def administrator(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_id = request.user.user_id  # Fetch the user ID
        user = get_object_or_404(users, user_id=user_id)
        role = user.role
        notifications_list = notifications.objects.all().order_by('-notification_created_at')
        # Redirect based on the user role
        if role == 'CSO Admin':
            user_organization = get_object_or_404(CSO_lists, cso_name = user.organization)
            notifications_list = notifications.objects.filter(notification_orgs=user_organization).order_by('-notification_created_at')
            days_fines, days_diff, months_diff = calculate_days_fines(user_organization)
            context = {'role': role, 'user_id': user_id, 'user_organization':user_organization, 'days_fines':days_fines, 'days_diff':days_diff, 'months_diff':months_diff, 'notifications_list':notifications_list}
            return render(request, 'cso_app/administrator/cso_admin/home.html', context)
        else:
            context = {'user_id': user_id, 'role': role, 'notifications_list':notifications_list}
            return render(request, 'cso_app/administrator/home.html', context)
    else:
        # Redirect unauthenticated users to the sign-in page
        return redirect('sign_in')

##############CSO ADMIN STARTS##################
def cso_admin_renewal(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    cso = user.organization
    cso_details = get_object_or_404(CSO_lists, cso_name = cso)
    days_fines, days_diff, months_diff = calculate_days_fines(cso_details)
    morethan3months = 0
    morethan3monthsfine = 0
    lessthan3monthsfine = 0
    late_report_fine = 0
    if days_diff >= 90 and days_diff <= 180:
        morethan3months = days_diff - 90
        morethan3monthsfine = (morethan3months * 200) + (90 * 100)
        late_report_fine = 30000
    elif days_diff > 180:
        morethan3months = days_diff - 90
        morethan3monthsfine = (morethan3months * 200) + (90 * 100)
        late_report_fine = 100000
    else:
        morethan3months = 0
        lessthan3monthsfine = days_diff * 100
        late_report_fine = 10000
    invalid_certificate_fines = cso_details.invalid_certificate_fines
    current_date = datetime.now().date()
    context = {'role': role, 'cso_details':cso_details, 'days_fines':days_fines, 'days_diff':days_diff, 'months_diff':months_diff, 'morethan3months':morethan3months, 'morethan3monthsfine':morethan3monthsfine, 'lessthan3monthsfine':lessthan3monthsfine, 'invalid_certificate_fines':int(invalid_certificate_fines), 'late_report_fine':late_report_fine, 'user':user, 'current_date':current_date}
    return render(request, 'cso_app/administrator/cso_admin/renewal_cso.html', context)

def cso_admin_pay_fees(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    cso = user.organization
    cso_details = get_object_or_404(CSO_lists, cso_name = cso)
    days_fines, days_diff, months_diff = calculate_days_fines(cso_details)
    morethan3months = 0
    morethan3monthsfine = 0
    lessthan3monthsfine = 0
    late_report_fine = 0
    if days_diff >= 90 and days_diff <= 180:
        morethan3months = days_diff - 90
        morethan3monthsfine = (morethan3months * 200) + (90 * 100)
        late_report_fine = 30000
    elif days_diff > 180:
        morethan3months = days_diff - 90
        morethan3monthsfine = (morethan3months * 200) + (90 * 100)
        late_report_fine = 100000
    else:
        morethan3months = 0
        lessthan3monthsfine = days_diff * 100
        late_report_fine = 10000
    invalid_certificate_fines = int(cso_details.invalid_certificate_fines)
    context = {'role': role, 'cso_details':cso_details, 'days_fines':days_fines, 'days_diff':days_diff, 'months_diff':months_diff, 'morethan3months':morethan3months, 'morethan3monthsfine':morethan3monthsfine, 'lessthan3monthsfine':lessthan3monthsfine, 'invalid_certificate_fines':invalid_certificate_fines, 'late_report_fine':late_report_fine, 'user':user}
    return render(request, 'cso_app/administrator/cso_admin/pay_fees.html', context)

def cso_admin_pay_fees_form(request):
    if request.method == 'POST':
        try:
            annual_report = request.FILES.get('annual_report', None)
            audit_report = request.FILES.get('audit_report', None)
            two_yrs_report = request.FILES.get('two_years_report', None)
            annual_general_report = request.FILES.get('annual_general_report', None)

            if annual_general_report is None:
                annual_general_report = 'annual_general_report/bg_astronaut.jpg'

            new_payment = cso_attachment_and_fees(
                cso_id=request.POST.get('cso_id_id'),
                cso_type=request.POST.get('cso_type'),
                cso_name=request.POST.get('cso_name'),
                user_name=request.POST.get('user_name'),
                user_email=request.POST.get('user_email'),
                user_cid=request.POST.get('user_cid'),
                mobile_number=request.POST.get('mobile_no'),
                delayed_days=request.POST.get('delayed_days'),
                renewal_fees=request.POST.get('renewal_fees'),
                late_renewal_fees=request.POST.get('late_renewal_fees'),
                amendment_type=request.POST.get('amendment_type'),
                amendment_fees=request.POST.get('amendment_fees'),
                late_report_fees=request.POST.get('late_report_fees'),
                overall_fines=request.POST.get('overall_fines'),
                annual_report=annual_report,
                audit_report=audit_report,
                two_yrs_report=two_yrs_report,
                annual_general_report=annual_general_report,
                status = "Submited",
                payment_status = "Pending"
            )
            new_payment.save()
            cso_name=request.POST.get('cso_name')
            user_id = request.user.user_id  # Fetch the user ID
            user = get_object_or_404(users, user_id=user_id)
            new_notification = notifications(
                notification_title = "Attachment files submitted!",
                notification_content = f"Report files for CSO {cso_name}",
                notification_view = "Both",
                notification_genre = "attachment_details",
                notification_orgs = cso_name,
                author = user.full_name,
                user_role = user.role
            )
            new_notification.save()
            return JsonResponse({"status": "success", "message": "Fees have been successfully submitted!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"})

    return HttpResponse(status=400)


def generate_certificate(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    cso = user.organization
    cso_details = get_object_or_404(CSO_lists, cso_name = cso)
    days_fines, days_diff, months_diff = calculate_days_fines(cso_details)
    morethan3months = 0
    morethan3monthsfine = 0
    lessthan3monthsfine = 0
    late_report_fine = 0
    if days_diff >= 90 and days_diff <= 180:
        morethan3months = days_diff - 90
        morethan3monthsfine = (morethan3months * 200) + (90 * 100)
        late_report_fine = 30000
    elif days_diff > 180:
        morethan3months = days_diff - 90
        morethan3monthsfine = (morethan3months * 200) + (90 * 100)
        late_report_fine = 100000
    else:
        morethan3months = 0
        lessthan3monthsfine = days_diff * 100
        late_report_fine = 10000
    invalid_certificate_fines = cso_details.invalid_certificate_fines
    current_date = datetime.now().date()
    context = {'role': role, 'cso_details':cso_details, 'days_fines':days_fines, 'days_diff':days_diff, 'months_diff':months_diff, 'morethan3months':morethan3months, 'morethan3monthsfine':morethan3monthsfine, 'lessthan3monthsfine':lessthan3monthsfine, 'invalid_certificate_fines':int(invalid_certificate_fines), 'late_report_fine':late_report_fine, 'user':user, 'current_date':current_date}
    return render(request, 'cso_app/administrator/cso_admin/certificate.html', context)




def calculate_days_fines(user_organization):
    validity_date = user_organization.cso_validity_date
    current_date = timezone.now().date()  # Use date() to get only the date part
    
    if validity_date > current_date:
        return 0
    else:
        difference = relativedelta(current_date, validity_date)
        months_diff = difference.years * 12 + difference.months
        days_diff = (current_date - validity_date).days
        
        # Calculate days fine
        if days_diff <= 90:
            days_fine = 100 * days_diff
        else:
            days_fine = (90 * 100) + ((days_diff - 90) * 200)

        if days_diff > 180:
            late_fine = 100000
            total_fine = late_fine + days_fine
        elif days_diff >= 90:
            late_fine = 30000
            total_fine = late_fine + days_fine
        else:
            late_fine = 10000
            total_fine = late_fine + days_fine
        
        return total_fine, days_diff, months_diff  # Return both fine and days_diff
    
def application_status(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    payments = cso_attachment_and_fees.objects.all()
    context = {'payments': payments, 'role': role}
    return render(request, 'cso_app/administrator/cso_admin/application_status.html', context)

def cso_annual_report(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    payments = cso_attachment_and_fees.objects.all()
    context = {'payments': payments, 'role': role}
    return render(request, 'cso_app/administrator/cso_admin/cso_annual_report.html', context)

def submit_annual_report(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    payments = cso_attachment_and_fees.objects.all()
    context = {'payments': payments, 'role': role}
    return render(request, 'cso_app/administrator/cso_admin/submit_annual_report.html', context)

##############CSO ADMIN ENDS##################

# Implement logic to calculate days and fines based on payment details
def attachment_history(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    payments = cso_attachment_and_fees.objects.all()
    context = {'payments': payments, 'role': role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/attachment_history.html', context)


def delete_attachment_fees(request, attachment_id):
    attachment = get_object_or_404(cso_attachment_and_fees, payment_id=attachment_id)
    attachment.delete()
    return redirect('attachment_history')

def fetch_payment_details(request):
    payment_id = request.GET.get('id')
    payment = cso_attachment_and_fees.objects.get(payment_id=payment_id)
    data = {
        'payment_id': str(payment.payment_id),  # UUID needs to be converted to string
        'cso_name': payment.cso_name,
        'fees_payment_type': payment.fees_payment_type,
        'amount_paid': payment.amount_paid,
        'account_number': payment.account_number,
        'account_name': payment.account_name,
        'bank_type': payment.bank_type,
        'user_email': payment.user_email,
        'mobile_number': payment.mobile_number,
        'payment_date': payment.payment_date.strftime('%Y-%m-%d'),  # Format as needed
        'status': payment.status,
        'reason': payment.reject_reasons
    }
    return JsonResponse(data)


import io
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

@csrf_exempt
def update_payment_details(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        try:
            payment = cso_attachment_and_fees.objects.get(payment_id=payment_id)
        except cso_attachment_and_fees.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Payment not found'})

        # Update payment details
        payment.cso_name = request.POST.get('cso_name')
        payment.fees_payment_type = request.POST.get('fees_payment_type')
        payment.overall_fines = request.POST.get('total_amount')
        payment.amount_paid = request.POST.get('amount_paid')
        payment.account_number = request.POST.get('account_number')
        payment.account_name = request.POST.get('account_name')
        payment.amendment_fees = request.POST.get('amendment_fees')
        payment.amendment_type = request.POST.get('amendment_type')
        payment.bank_type = request.POST.get('bank_type')
        payment.user_email = request.POST.get('user_email')
        payment.mobile_number = request.POST.get('mobile_number')
        payment.status = request.POST.get('status')
        payment.reject_reasons = request.POST.get('rejection_reason')
        
        # Generate a random refNo
        year = datetime.now().year
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(14)])
        ref_no = f"CSOA-{year}-{random_number}"
        payment.ref_no = ref_no
        payment.save()

        subject = "Payment & Documents Verified Successfully!"
        sender = "devilboi150@gmail.com"
        receiver = [payment.user_email]

        if payment.status == 'Approved':
            message = f"""
                Hi {payment.user_name},
                Your application renewal and payment amounting to {payment.overall_fines} has been approved. 
                Thank you for your timely payment.
            """
            token = get_access_token()
            if token:
                # Construct the payment request
                payment_url = 'https://staging-datahub-apim.tech.gov.bt/birms_paymentserviceapi/1.0.0/paymentdetails/create'
                payment_headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                payment_data = {
                    "platform": "test3",
                    "refNo": ref_no,
                    "taxPayerNo": "DTH3733",
                    "taxPayerDocumentNo": "1",
                    "paymentRequestDate": datetime.now().date().isoformat(),
                    "agencyCode": "CTH4468",
                    "payerEmail": payment.user_email,
                    "mobileNo": payment.mobile_number,
                    "totalPayableAmount": payment.overall_fines,
                    "paymentDueDate": "null",
                    "taxPayerName": payment.account_name,
                    "paymentLists": [
                        {
                            "serviceCode": "100042",
                            "description": "Registration Fee",
                            "payableAmount": payment.overall_fines
                        }
                    ],
                    "code": "moenr"
                }
                response = requests.post(payment_url, headers=payment_headers, json=payment_data)
                if response.status_code == 200:
                    response_data = response.json()
                    redirect_url = response_data.get('content', {}).get('redirectUrl')
                    payment_advice_no = response_data.get('content', {}).get('paymentAdviceNo')
                    payment_advice_date = response_data.get('content', {}).get('paymentAdviceDate')
                    payment.payment_advice_date = payment_advice_date
                    payment.payment_advice_no = payment_advice_no
                    payment.save()
                    # Include the redirectUrl in the email
                    message += f"\nPlease complete your payment by visiting the following link:\n{redirect_url}"
                    ##This is to save the notifications details
                    cso_name = request.POST.get('cso_name')
                    overall_amount = request.POST.get('total_amount')
                    new_notification = notifications(
                        notification_title = "Appoved Documents!",
                        notification_content = f"Documents for {cso_name} and payment of nu. {overall_amount} has been approved!",
                        notification_view = "Admin",
                        notification_orgs = cso_name,
                        notification_genre = "attachment_details"
                    )
                    new_notification.save()
                else:
                    print("Payment failed:", response.text)
            else:
                message += "\nHowever, we couldn't process the payment request. Please try again later."
        else:
            message = f"""
                Hi {payment.user_name},
                Your application for the payment amounting to {payment.user_name} has been rejected. 
                Reason: {payment.reject_reasons if payment.reject_reasons else 'No reason provided.'}
            """

        # Send the email
        send_mail(
            subject, 
            message, 
            sender,
            receiver, 
            fail_silently=False
        )
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def recieve_payment_details(request):
    agency_code = 'CTH4468'  # Replace with your actual agency code
    reference_number = request.GET.get('referenceNumber')  # Or however you're passing the reference number

    if not reference_number:
        return JsonResponse({'success': False, 'error': 'Reference number is required'})

    api_url = f"https://staging-datahub-apim.tech.gov.bt/birms_paymentserviceapi/1.0.0/paymentreferenceNumber/{agency_code}/{reference_number}"

    try:
        # Make the GET request to the API
        response = requests.get(api_url, headers={'Accept': 'application/json'})

        if response.status_code == 200:
            # If the request is successful, return the API response
            payment_details = response.json()
            return JsonResponse({'success': True, 'payment_details': payment_details})
        else:
            # Handle any errors returned by the API
            return JsonResponse({'success': False, 'error': 'Failed to retrieve payment details', 'details': response.text})

    except requests.RequestException as e:
        # Handle any exceptions during the request
        return JsonResponse({'success': False, 'error': str(e)})

import re
def extract_uuid(queryset_string):
    # Use regular expression to find the UUID pattern
    match = re.search(r"UUID\('([a-f0-9\-]+)'\)", queryset_string)
    if match:
        return match.group(1)
    else:
        return None

from django.db.models import Q

def registered_users(request):
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    user_list = users.objects.filter(Q(status="Active") | Q(status="Inactive") | Q(status="New User"))
    user_id_queryset = users.objects.all().values_list('user_id', flat=True)
    user_role = user_roles.objects.all()
    organization = organizations.objects.all()
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    # Assuming there's only one user_id and we want to get its string representation
    user_id = str(user_id_queryset[0]) if user_id_queryset else None    
    context = {'user_list': user_list, 'user_id':user_id, 'user_role':user_role, 'organization':organization, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/system_user.html', context)


def registered_users_cso_admin(request):
    user_id_queryset = users.objects.all().values_list('user_id', flat=True)
    user_role = user_roles.objects.all()
    organization = organizations.objects.all()
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    user_organization = user.organization
    print("THis is the user organization: ", user_organization)

    user_list = users.objects.filter(organization=user_organization)
    role = user.role
    # Assuming there's only one user_id and we want to get its string representation
    user_id = str(user_id_queryset[0]) if user_id_queryset else None    
    context = {'user_list': user_list, 'user_id':user_id, 'user_role':user_role, 'organization':organization, 'role':role, 'user_organization':user_organization}
    return render(request, 'cso_app/administrator/cso_admin/registered_users_cso_admin.html', context)

def delete_user(request, id):
    if request.method == 'POST':
        user = get_object_or_404(users, user_id=id)
        print("This is the user: ", user)
        user.status = "Deleted!"
        user.save()
        # user.delete()
        return HttpResponse(status=204)  # Return no content on successful deletion
    else:
        return HttpResponse(status=405)  # Method not allowed if not POST
    
def check_cid(request):
    cid = request.GET.get('cid', None)
    if cid:
        exists = users.objects.filter(CID=cid).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

@login_required
def add_new_user(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    roles = user_roles.objects.all()
    organization_list = organizations.objects.all()
    error_message = ''
    try:
        if request.method == 'POST':
            cid = request.POST.get('cid')
            full_name = request.POST.get('full_name')
            date_of_birth = request.POST.get('dob')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            position_title = request.POST.get('position_title')
            mobile_number = request.POST.get('mobile_no')
            user_role = request.POST.get('user_role')
            organization = request.POST.get('organization')
            status = request.POST.get('status')
            profile_pic = request.FILES.get('profile_pic')
            # Hash the password before saving
            hashed_password = make_password(password)
            
            new_user = users(
                CID=cid,
                full_name=full_name,
                dob=date_of_birth,
                username=username,
                password=hashed_password,
                email=email,
                position_title=position_title,
                mobile_no=mobile_number,
                role=user_role,
                organization=organization,
                status=status,
                profile_pic=profile_pic
            )
            new_user.save()
            new_notification = notifications(
                notification_title="Created A New User",
                notification_content=f"User for name:{full_name} role:{user_role} for organization:{organization}, successfully created!",
                notification_view="Admin",
                notification_genre="user_details"
            )
            new_notification.save()


            subject = "User Created Successfully!"
            sender = "devilboi150@gmail.com"
            receiver = [email]  # Make receiver a list
            message = f"""
                        Hi {full_name},
                        Congratulations! Your account for {username} has been created successfully!
                        Your login credentials are: 
                        Username: {username} 
                        Password: {password}
                    """
            send_mail(
                subject, 
                message, 
                sender,
                receiver, 
                fail_silently=False
            )
            return redirect('registered_users')  # Redirect to a success page or another appropriate page
    except Exception as e:
        return HttpResponse("Can't Have Same Username Please Change: ", e)

    context = {'roles': roles, 'organization_list': organization_list, 'error_message': error_message, 'role':role,'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/add_new_user.html', context)

@login_required
def cso_add_new_user(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    roles = user_roles.objects.all()
    # Filter to get the organization of the current user
    organization_list = get_object_or_404(CSO_lists, cso_name=user.organization)
    print("This is the organization: ", organization_list)

    error_message = ''
    try:
        if request.method == 'POST':
            cid = request.POST.get('cid')
            full_name = request.POST.get('full_name')
            date_of_birth = request.POST.get('dob')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            position_title = request.POST.get('position_title')
            mobile_number = request.POST.get('mobile_no')
            user_role = request.POST.get('user_role')
            organization = request.POST.get('organization')
            status = request.POST.get('status')
            profile_pic = request.FILES.get('profile_pic')

            # Hash the password before saving
            hashed_password = make_password(password)
            
            new_user = users(
                CID=cid,
                full_name=full_name,
                dob=date_of_birth,
                username=username,
                password=hashed_password,
                email=email,
                position_title=position_title,
                mobile_no=mobile_number,
                role=user_role,
                organization=organization,
                status=status,
                profile_pic=profile_pic
            )
            new_user.save()

            subject = "User Created Successfully!"
            sender = "devilboi150@gmail.com"
            receiver = [email]  # Make receiver a list
            message = f"""
                        Hi {full_name},
                        Congratulations! Your account for {username} has been created successfully!
                        Your login credentials are: 
                        Username: {username} 
                        Password: {password}
                    """
            send_mail(
                subject, 
                message, 
                sender,
                receiver, 
                fail_silently=False
            )
            return redirect('registered_users')  # Redirect to a success page or another appropriate page
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

    context = {'roles': roles, 'organization_list': organization_list, 'error_message': error_message, 'role': role}
    return render(request, 'cso_app/administrator/cso_admin/add_new_user.html', context)

def master_data(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    processes = system_process.objects.all()
    gewogs = gewog.objects.all()
    dzongkhag = dzongkhags.objects.all()
    context = {'processes': processes, 'gewogs':gewogs, 'dzongkhag':dzongkhag, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/master_data.html', context)


def user_details(request, user_id):
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    user = users.objects.get(user_id=user_id)
    print("This is the user: ", user)
    dob = user.dob.strftime("%Y-%m-%d")
    created_date = user.created_date.strftime("%Y-%m-%d")  
    user_id_queryset = users.objects.all().values_list('user_id', flat=True)
    # Assuming there's only one user_id and we want to get its string representation
    user_id = str(user_id_queryset[0]) if user_id_queryset else None
    user_idd = request.user.user_id  # Fetch the user ID
    current_user = get_object_or_404(users, user_id=user_idd)
    role = current_user.role
    context = {'user': user, 'dob':dob, 'created_date':created_date, 'user_id':user_id, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/user_details.html', context)

def user_settings(request, user_id):
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    user = get_object_or_404(users, user_id=user_id)
    print("This is the user: ", user)
    dob = user.dob.strftime("%Y-%m-%d")
    created_date = user.created_date.strftime("%Y-%m-%d")  
    user_id_queryset = users.objects.all().values_list('user_id', flat=True)
    user_id = str(user_id_queryset[0]) if user_id_queryset else None  
    user_idd = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_idd)
    role = user.role
    context = {'user': user, 'dob':dob, 'created_date':created_date, 'user_id':user_id, 'role':role,'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/user_settings.html', context)

def update_profile(request, user_id):
    user = get_object_or_404(users, user_id=user_id)
    print("This is the user details: ", user)
    if request.method == 'POST':
        # Retrieve data from POST request
        cid = request.POST.get('cid')
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('dob')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        position_title = request.POST.get('position_title')
        mobile_number = request.POST.get('mobile_no')
        user_role = request.POST.get('user_role')
        organization = request.POST.get('organization')
        status = request.POST.get('status')
        profile_pic = request.FILES.get('profile_pic')  # If updating profile pic

        # Update user object with new data
        user.CID = cid
        user.username = username
        user.full_name = full_name
        user.dob = date_of_birth
        user.username = username
        user.email = email
        user.position_title = position_title
        user.mobile_no = mobile_number
        user.role = user_role
        user.organization = organization
        user.status = status

        if password:
            user.password = make_password(password)  # Hash the new password

        if profile_pic:
            user.profile_pic = profile_pic  # Update profile pic if provided

        # Save the updated user object
        user.save()
        new_notifications = notifications(
            notification_title = f"Profile Updated for username: {username}",
            notification_content = "Successfully updated user profile!",
            notification_view = "Admin",
            notification_orgs = "organization",
            notification_genre = "user_details"
        )
        new_notifications.save()
        # Redirect to user details page after successful update
        return redirect(reverse('user_details', args=[user_id]))  # Redirect to the profile page or any other page if the request is not POST

def create_new_process(request):
    if request.method == 'POST':
        process_name = request.POST.get('process_name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        new_process = system_process(
            process=process_name,
            description=description,
            duration=duration
        )
        new_process.save()
    else:
        error_msg="Something went wrong while trying to save a new process in the database"
        context = {'error_msg':error_msg}
        return redirect('master_data', context)
    return redirect('master_data')

def delete_process(request, process_id):
    process = get_object_or_404(system_process, id=process_id)
    if request.method == 'POST':
        process.delete()

    return redirect('master_data')  # Redirect to the master data page after deletion

def update_process(request):
    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        process_name = request.POST.get('process_name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        print("This is the process data: ", process_id, process_name, description, duration)
        process = get_object_or_404(system_process, id=process_id)
        process.process = process_name
        process.description = description
        process.duration = duration
        process.save()

        return redirect('master_data')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update a process in the database"
        context = {'error_msg':error_msg}
        return redirect('master_data', context)  # Redirect if not POST request
    
def update_gewog(request):
    if request.method == 'POST':
        gewog_id = request.POST.get('gewog_id')
        gewog_name = request.POST.get('gewog_name')
        dzongkhag = request.POST.get('gewog_dzongkhag')
        status = request.POST.get('status')
        
        gewogs = get_object_or_404(gewog, gewog_id=gewog_id)
        gewogs.gewog_name = gewog_name
        gewogs.dzongkhag = dzongkhag
        gewogs.status = status
        gewogs.save()

        return redirect('master_data')  # Redirect after successful update
    else:
        return redirect('master_data')  # Redirect if not POST request

def delete_gewog(request, gewog_id):
    if request.method == 'POST':
        gewogs = get_object_or_404(gewog, gewog_id=gewog_id)
        gewogs.delete()
        return HttpResponse(status=204)  # Return no content on successful deletion
    else:
        return HttpResponse(status=405)  # Method not allowed if not POST
    
def update_dzongkhag(request):
    if request.method == 'POST':
        dzongkhag_id = request.POST.get('dzongkhag_id')
        dzongkhag_name = request.POST.get('dzongkhag_name')
        
        dzongkhag = get_object_or_404(dzongkhags, dzongkhag_id=dzongkhag_id)
        dzongkhag.dzongkhag_name = dzongkhag_name
        dzongkhag.save()
        
        return redirect('master_data')

def delete_dzongkhag(request, dzongkhag_id):
    if request.method == 'POST':
        dzongkhag = get_object_or_404(dzongkhags, dzongkhag_id=dzongkhag_id)
        dzongkhag.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})


def login_history(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    sign_in_details = SignInDetails.objects.all()
    context = {'sign_in_details':sign_in_details, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/login_history.html', context)

def audit_trials(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_data = notifications.objects.all() 
    context = {'role':role, 'notifications_data':notifications_data}
    return render(request, 'cso_app/administrator/audit_trials.html', context)

def cso_master_links(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    cso_type = cso_types.objects.all()
    thematic_areas = thematic_area.objects.all()
    attachment = profile_attachments.objects.all()
    closing_type = cso_closing_type.objects.all()
    context = {'cso_type':cso_type, 'thematic_areas':thematic_areas, 'attachment':attachment,'closing_type':closing_type, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/cso_master/cso_master_links.html', context)

def cso_ranks_home(request):
    current_date = datetime.now().year
    previous_year = current_date - 1
    cso_ranks = cso_rankings.objects.all().order_by('rank')
    context = {'cso_ranks':cso_ranks, 'current_date':current_date, 'previous_year':previous_year}
    return render(request, 'cso_app/cso_rank.html', context)

def cso_ranks(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    cso_list = CSO_lists.objects.all()
    cso_ranks = cso_rankings.objects.all().order_by('rank')
    existing_cso_ids = cso_rankings.objects.values_list('cso_id_id', flat=True)

    context = {'cso_list':cso_list, 'cso_ranks':cso_ranks, 'existing_cso_ids':existing_cso_ids,'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/cso_master/cso_ranks.html', context)

def save_cso_rank(request):
    if request.method == 'POST':
        print("reaching here!!")
        cso_id = request.POST.get('cso_name')
        cso_name = request.POST.get('cso_name_hidden')  # Retrieve the CSO name from the hidden input
        score = request.POST.get('cso_score')  # Ensure form field name matches
        print("This is the cso_ID: ", cso_id)
        # Check if score is a valid integer
        try:
            score = int(score)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid score value'}, status=400)
        
        # Create a new CSO ranking instance
        new_cso_rank = cso_rankings(
            cso_id_id=cso_id,
            cso_name=cso_name,  # Save the CSO name
            score=score
        )
        new_cso_rank.save()
        # Recalculate ranks after saving a new ranking
        recalculate_ranks()
        # Redirect back to the form view with a success flag
        new_notifications = notifications(
            notification_title = f"CSO has been ranked!",
            notification_content = f"Successfully ranked CSO: {cso_name}!",
            notification_view = "Admin",
            notification_orgs = "organization",
            notification_genre = "attachment_details"
        )
        new_notifications.save()
        return redirect('cso_ranks')  # Replace with your form view name

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def recalculate_ranks():
    # Retrieve all CSO rankings ordered by score in descending order
    cso_ranks = cso_rankings.objects.all().order_by('-score')

    # Extract unique scores from the QuerySet and sort them in descending order
    unique_scores = sorted(set(cso.score for cso in cso_ranks), reverse=True)

    # Dictionary to store the rank for each score
    score_to_rank = {score: rank + 1 for rank, score in enumerate(unique_scores)}

    # Debug print to verify the score to rank mapping
    print("Score to Rank Mapping:", score_to_rank)

    # Update the ranks in the database
    for cso in cso_ranks:
        cso.rank = score_to_rank[cso.score]
        cso.save()

    print("Ranks recalculated successfully.")
    return None






def create_new_cso_type(request):
    if request.method == 'POST':
        cso_name = request.POST.get('cso_name')
        cso_prefix = request.POST.get('cso_prefix')
        new_cso = cso_types(
            cso_name=cso_name,
            cso_prefix=cso_prefix
        )
        new_cso.save()
    else:
        error_msg="Something went wrong while trying to save a new CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)
    return redirect('cso_master_links') 

def delete_cso(request, cso_id):
    cso_type = get_object_or_404(cso_types, cso_id=cso_id)
    print("This is the CSO data: ", cso_type, cso_id)
    if request.method == 'POST':
        cso_type.delete()

    return redirect('cso_master_links')  # Redirect to the master data page after deletion

def update_cso(request):
    if request.method == 'POST':
        cso_id = request.POST.get('cso_id')
        cso_name = request.POST.get('cso_name')
        cso_prefix = request.POST.get('cso_prefix')
        status = request.POST.get('status')  # Change this line to get 'status' instead of 'duration'
        cso = get_object_or_404(cso_types, cso_id=cso_id)
        cso.cso_id = cso_id
        cso.cso_name = cso_name
        cso.cso_prefix = cso_prefix
        cso.cso_status = status
        cso.save()
        return redirect('cso_master_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update the CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)  # Redirect if not POST request
    
def create_new_thematic_cso(request):
    if request.method == 'POST':
        cso_name = request.POST.get('cso_name')
        new_cso = thematic_area(
            cso_name=cso_name
        )
        new_cso.save()
    else:
        error_msg="Something went wrong while trying to save a new CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)
    return redirect('cso_master_links') 

def delete_thematic_cso(request, cso_id):
    cso_type = get_object_or_404(thematic_area, cso_id=cso_id)
    if request.method == 'POST':
        cso_type.delete()
    return redirect('cso_master_links')  # Redirect to the master data page after deletion

def update_thematic_cso(request):
    if request.method == 'POST':
        cso_id = request.POST.get('cso_id')
        cso_name = request.POST.get('cso_name')
        status = request.POST.get('status')  # Change this line to get 'status' instead of 'duration'
        cso = get_object_or_404(thematic_area, cso_id=cso_id)
        cso.cso_id = cso_id
        cso.cso_name = cso_name
        cso.cso_status = status
        cso.save()
        return redirect('cso_master_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update the CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)  # Redirect if not POST request
    
def create_new_attachment(request):
    if request.method == 'POST':
        attachment_name = request.POST.get('attachment_name')
        attachment_description = request.POST.get('attachment_description')
        public_display = request.POST.get('inlineRadioOptions')  # Fetch the radio button value
        process_option = request.POST.get('process_option')
        # Fetch checkbox values as a list
        cso_types_list = request.POST.getlist('cso_types')
        
        # Join the list into a single string
        cso_types = ', '.join(cso_types_list)
        new_attachment = profile_attachments(
            cso_attachment_name = attachment_name,
            cso_attachment_description = attachment_description,
            public_display = public_display,
            process = process_option,
            cso_type = cso_types
        )
        new_attachment.save()
    else:
        error_msg="Something went wrong while trying to save a new CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)
    return redirect('cso_master_links') 

def delete_attachment(request, cso_attachment_id):
    profile_attachment = get_object_or_404(profile_attachments, cso_attachment_id=cso_attachment_id)
    if request.method == 'POST':
        profile_attachment.delete()
    return redirect('cso_master_links') 

def update_cso_attachment(request):
    if request.method == 'POST':
        cso_attachment_id = request.POST.get('cso_attachment_id')
        cso_attachment_name = request.POST.get('cso_attachment_name')
        cso_attachment_description = request.POST.get('cso_attachment_description')
        public_display = request.POST.get('inlineRadioOptions')  # Fetch the radio button value
        process_option = request.POST.get('process_option')
        # Fetch checkbox values as a list
        cso_types_list = request.POST.getlist('cso_types')
        # Join the list into a single string
        cso_type = ', '.join(cso_types_list)
        status = request.POST.get('status')  # Change this line to get 'status' instead of 'duration'
        attachment = get_object_or_404(profile_attachments, cso_attachment_id=cso_attachment_id)
        attachment.cso_attachment_id = cso_attachment_id
        attachment.cso_attachment_name = cso_attachment_name
        attachment.cso_attachment_description = cso_attachment_description
        attachment.public_display = public_display
        attachment.process_option = process_option
        attachment.cso_type = cso_type
        attachment.status = status
        attachment.save()
        return redirect('cso_master_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update the CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)  # Redirect if not POST request
    
def create_new_cso_closing(request):
    if request.method == 'POST':
        closing_type = request.POST.get('closing_type')
        closing_description = request.POST.get('closing_description')
        # Fetch checkbox values as a list
        new_closing_type = cso_closing_type(
            cso_closing_type = closing_type,
            cso_closing_description = closing_description
        )
        new_closing_type.save()
    else:
        error_msg="Something went wrong while trying to save a new CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)
    return redirect('cso_master_links') 

def delete_closing_type(request, cso_closing_id):
    cso_closing_types = get_object_or_404(cso_closing_type, cso_closing_id=cso_closing_id)
    if request.method == 'POST':
        cso_closing_types.delete()
    return redirect('cso_master_links') 

def update_closing_type(request):
    if request.method == 'POST':
        cso_closing_id = request.POST.get('cso_closing_id')
        cso_closing_types = request.POST.get('cso_closing_type')
        cso_closing_description = request.POST.get('cso_closing_description')
        status = request.POST.get('status')  # Change this line to get 'status' instead of 'duration'
        closing = get_object_or_404(cso_closing_type, cso_closing_id=cso_closing_id)
        closing.cso_closing_id = cso_closing_id
        closing.cso_closing_type = cso_closing_types
        closing.cso_closing_description = cso_closing_description
        closing.status = status
        closing.save()
        return redirect('cso_master_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update the CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('cso_master_links', context)  # Redirect if not POST request
    
def certificate_collection(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    certificate_applications = certificate_application.objects.all()
    context = {'certificate_applications':certificate_applications, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/public certificate application/public_collection_certificate_applications.html', context)

from django.contrib import messages

def upload_certificate_application(request, application_id):
    application = get_object_or_404(certificate_application, pk=application_id)

    if request.method == 'POST' and request.FILES['certificate_application']:
        uploaded_file = request.FILES['certificate_application']
        application.certificate_application = uploaded_file
        application.save()
        messages.success(request, 'File has been successfully uploaded.')
        return redirect('certificate/collectionlist/')  # Redirect to the list view or any other page

    return render(request, 'cso_app/administrator/public_certificate_application/public_collection_certificate_applications.html', {'application': application})

def cso_list(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    pbo = CSO_lists.objects.filter(cso_type = 'PBO')
    mbo = CSO_lists.objects.filter(cso_type = 'MBO')
    context = {'pbo':pbo, 'mbo':mbo, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/cso_list/cso_list.html', context)

def cso_detail(request, id):
    cso = get_object_or_404(CSO_lists, pk=id)
    user_id = request.user.user_id  # Fetch the user ID
    userz = get_object_or_404(users, user_id=user_id)
    role = userz.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')

    print(f"This is the role: {role}")
    trustees = cso.trustees.all()  # This uses the related_name 'trustees'
    payments = cso_attachment_and_fees.objects.filter(cso_name=cso)
    cso_types = cso.cso_type
    context = {'cso':cso, 'trustees': trustees,'notifications_list':notifications_list, 'payments': payments, 'cso_types':cso_types, role:'role'}
    return render(request, 'cso_app/administrator/cso_list/cso_details.html', context)

def update_pbos(request):
    if request.method == 'POST':
        pbo_id = request.POST.get('pbo_cso_id')
        pbo_name = request.POST.get('pbo_cso_name')
        pbo_email = request.POST.get('pbo_cso_email')
        pbo_fixed_phone = request.POST.get('pbo_fixed_phone')
        pbo_po_box = request.POST.get('pbo_po_box')
        pbo_public_mobile = request.POST.get('pbo_public_mobile')
        pbo_fax = request.POST.get('pbo_fax')
        pbo_public_email = request.POST.get('pbo_public_email')
        pbo_website = request.POST.get('pbo_website')
        pbo_toll_free_no = request.POST.get('pbo_toll_free_no')
        pbo_address = request.POST.get('pbo_address')
        pbo_ex_name = request.POST.get('pbo_ex_name')
        pbo_ex_id = request.POST.get('pbo_ex_id')
        pbo_ex_email = request.POST.get('pbo_ex_email')
        pbo_ex_phone = request.POST.get('pbo_ex_phone')
        pbo_focal_name = request.POST.get('pbo_focal_name')
        pbo_focal_id = request.POST.get('pbo_focal_id')
        pbo_focal_email = request.POST.get('pbo_focal_email')
        pbo_focal_phone = request.POST.get('pbo_focal_phone')
        areas_of_operations = request.POST.get('areas_of_operations')
        pbo_purpose = request.POST.get('pbo_purpose')
        pbo_objectives = request.POST.get('pbo_objectives')
        pbo_remarks = request.POST.get('pbo_remarks')
        invalid_certificate_fines = request.POST.get('invalid_certificate_fines')
        status = request.POST.get('pbo_cso_status')

        pbos = get_object_or_404(CSO_lists, cso_id=pbo_id)

        # Update the fields
        pbos.cso_name = pbo_name
        pbos.cso_email = pbo_email
        pbos.fixed_phone_no = pbo_fixed_phone
        pbos.po_box = pbo_po_box
        pbos.public_contact = pbo_public_mobile
        pbos.fax = pbo_fax
        pbos.public_email = pbo_public_email
        pbos.cso_url = pbo_website
        pbos.toll_free_no = pbo_toll_free_no
        pbos.address = pbo_address
        pbos.executive_director = pbo_ex_name
        pbos.executive_ID = pbo_ex_id
        pbos.executive_email = pbo_ex_email
        pbos.executive_phone = pbo_ex_phone
        pbos.cso_focal_name = pbo_focal_name
        pbos.cso_focal_ID = pbo_focal_id
        pbos.cso_focal_email = pbo_focal_email
        pbos.cso_focal_phone = pbo_focal_phone
        pbos.operation_places = areas_of_operations
        pbos.purpose = pbo_purpose
        pbos.objectives = pbo_objectives
        pbos.remarks = pbo_remarks
        pbos.invalid_certificate_fines = invalid_certificate_fines
        pbos.status = status

        pbos.save()

        return redirect('cso_list')  # Redirect after successful update
    else:
        error_msg = "Something went wrong while trying to update the CSO PBOs in the database"
        context = {'error_msg': error_msg}
        return redirect('cso_list', context)  # Redirect if not POST request

def update_mbos(request):
    if request.method == 'POST':
        mbo_id = request.POST.get('mbo_cso_id')
        mbo_name = request.POST.get('mbo_cso_name')
        mbo_email = request.POST.get('mbo_cso_email')
        mbo_fixed_phone = request.POST.get('mbo_fixed_phone')
        mbo_po_box = request.POST.get('mbo_po_box')
        mbo_public_mobile = request.POST.get('mbo_public_mobile')
        mbo_fax = request.POST.get('mbo_fax')
        mbo_public_email = request.POST.get('mbo_public_email')
        mbo_website = request.POST.get('mbo_website')
        mbo_toll_free_no = request.POST.get('mbo_toll_free_no')
        mbo_address = request.POST.get('mbo_address')
        mbo_ex_name = request.POST.get('mbo_ex_name')
        mbo_ex_id = request.POST.get('mbo_ex_id')
        mbo_ex_email = request.POST.get('mbo_ex_email')
        mbo_ex_phone = request.POST.get('mbo_ex_phone')
        mbo_focal_name = request.POST.get('mbo_focal_name')
        mbo_focal_id = request.POST.get('mbo_focal_id')
        mbo_focal_email = request.POST.get('mbo_focal_email')
        mbo_focal_phone = request.POST.get('mbo_focal_phone')
        areas_of_operations = request.POST.get('areas_of_operations')
        mbo_purpose = request.POST.get('mbo_purpose')
        mbo_objectives = request.POST.get('mbo_objectives')
        mbo_remarks = request.POST.get('mbo_remarks')
        mbo_invalid_certificate = request.POST.get('mbo_invalid_certificate_fines')
        status = request.POST.get('mbo_cso_status')

        mbos = get_object_or_404(CSO_lists, cso_id=mbo_id)

        # Update the fields
        mbos.cso_name = mbo_name
        mbos.cso_email = mbo_email
        mbos.fixed_phone_no = mbo_fixed_phone
        mbos.po_box = mbo_po_box
        mbos.public_contact = mbo_public_mobile
        mbos.fax = mbo_fax
        mbos.public_email = mbo_public_email
        mbos.cso_url = mbo_website
        mbos.toll_free_no = mbo_toll_free_no
        mbos.address = mbo_address
        mbos.executive_director = mbo_ex_name
        mbos.executive_ID = mbo_ex_id
        mbos.executive_email = mbo_ex_email
        mbos.executive_phone = mbo_ex_phone
        mbos.cso_focal_name = mbo_focal_name
        mbos.cso_focal_ID = mbo_focal_id
        mbos.cso_focal_email = mbo_focal_email
        mbos.cso_focal_phone = mbo_focal_phone
        mbos.operation_places = areas_of_operations
        mbos.purpose = mbo_purpose
        mbos.objectives = mbo_objectives
        mbos.remarks = mbo_remarks
        mbos.invalid_certificate_fines = mbo_invalid_certificate
        mbos.status = status

        mbos.save()

        return redirect('cso_list')  # Redirect after successful update
    else:
        error_msg = "Something went wrong while trying to update the CSO mbos in the database"
        context = {'error_msg': error_msg}
        return redirect('cso_list', context)  # Redirect if not POST request

def update_trustees(request, cso_id):
    cso = get_object_or_404(CSO_lists, cso_id=cso_id)
    trustees = cso.trustees.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        appointed_date = request.POST.get('appointed_date')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        other_trusteeship = request.POST.get('other_trusteeship')
        if email:
            trustee = Trustee(
                cso_id=cso,
                name=name,
                position=position,
                appointed_date=appointed_date,
                phone_no=phone_no,
                email=email,
                other_trusteeship=other_trusteeship,
            )
            trustee.save()
            return JsonResponse({'success': True, 'message': 'Trustee details updated successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Email is required.'})
    else:
        context = {
            'cso': cso,
            'trustees': trustees,
        }
        return render(request, 'cso_app/cso_list/cso_details.html', context)

def delete_cso_list(request, cso_id):
    cso_details = get_object_or_404(CSO_lists, cso_id=cso_id)
    if request.method == 'POST':
        cso_details.delete()
    return redirect('cso_list')  # Redirect to the master data page after deletion
#Manage CSO Details
def creating_new_cso(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    cso_type = cso_types.objects.all()
    thematic_areas = thematic_area.objects.all()
    context = {'cso_type':cso_type, 'thematic_areas':thematic_areas, 'role':role, 'notifications_list':notifications_list}
    return render(request, 'cso_app/manage_cso/create_a_cso.html', context)

def check_cso_name(request):
    cso_name = request.GET.get('cso_name', None)
    exists = CSO_lists.objects.filter(cso_name=cso_name).exists()
    return JsonResponse({'exists': exists})

def creating_new_cso_form(request):
    if request.method == 'POST':
        cso_type = request.POST.get('cso_type')
        cso_name = request.POST.get('cso_name')
        cso_acronym = request.POST.get('cso_acronym')
        cso_focal = request.POST.get('cso_focal')
        cso_contact = request.POST.get('cso_contact')
        cso_email = request.POST.get('cso_email')
        cso_url = request.POST.get('cso_url')
        cso_logo = request.FILES.get('cso_logo')
        thematic_area = request.POST.get('cso_thematic')
        validity_date = datetime.now() + timedelta(days=365)

        if CSO_lists.objects.filter(cso_name=cso_name).exists():
            messages.error(request, f"CSO name '{cso_name}' already exists. Please choose a different name.")
            return redirect('creating_new_cso')
        try:
            new_cso = CSO_lists(
                cso_name=cso_name,
                cso_type=cso_type,
                cso_acronym=cso_acronym,
                cso_focal=cso_focal,
                cso_contact=cso_contact,
                cso_email=cso_email,
                cso_url=cso_url,
                cso_logo=cso_logo,
                thematic_area=thematic_area,
                status='new',
                cso_validity_date=validity_date
            )
            new_cso.save()
            messages.success(request, f"CSO '{cso_name}' has been successfully registered.")
        except Exception as e:
            messages.error(request, f"Error while saving CSO: {e}")

        return redirect('creating_new_cso')
    else:
        messages.error(request, "Invalid request method. Refresh & try again.")
        return redirect('creating_new_cso')

def financial_links(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    financial_classes = financial_class.objects.all()
    financial_groups = financial_group.objects.all()
    financial_attachment = financial_attachments.objects.all()
    context = {'role':role, 'financial_classes':financial_classes, 'financial_groups':financial_groups, 'financial_attachment':financial_attachment, 'notifications_list':notifications_list}
    return render(request, 'cso_app/administrator/annual_report_master/financial_links.html',context)

def update_financial_class(request):
    if request.method == 'POST':
        financialId = request.POST.get('financial_id')
        financialClass = request.POST.get('financial_class')
        financialDescription = request.POST.get('financial_description')
        financial_klass = get_object_or_404(financial_class, financial_id=financialId)
        financial_klass.financial_id = financialId
        financial_klass.financial_class = financialClass
        financial_klass.financial_description = financialDescription
        financial_klass.save()
        return redirect('financial_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to financial class in the database"
        context = {'error_msg':error_msg}
        return redirect('financial_links', context)  # Redirect if not POST request

def create_new_financial_group(request):
    if request.method == 'POST':
        financialGroup = request.POST.get('financial_group')
        financialDescription = request.POST.get('financial_description')
        financialClass = request.POST.get('financial_class')
        new_finance_group = financial_group(
            financial_group_name=financialGroup,
            financial_description = financialDescription,
            financial_group_class = financialClass
        )
        new_finance_group.save()
    else:
        error_msg="Something went wrong while trying to save a new CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('financial_links', context)
    return redirect('financial_links') 

def delete_financial_group(request, financial_group_id):
    financialGroup = get_object_or_404(financial_group, financial_group_id=financial_group_id)
    if request.method == 'POST':
        financialGroup.delete()
    return redirect('financial_links')  # Redirect to the master data page after deletion

def update_financial_group(request):
    if request.method == 'POST':
        financial_group_id = request.POST.get('financial_group_id')
        financial_group_name = request.POST.get('financial_group_name')
        financial_description = request.POST.get('financial_description')
        financial_group_class = request.POST.get('financial_group_class')
        status = request.POST.get('status')  # Change this line to get 'status' instead of 'duration'
        financeGroup = get_object_or_404(financial_group, financial_group_id=financial_group_id)
        financeGroup.financial_group_id = financial_group_id
        financeGroup.financial_group_name = financial_group_name
        financeGroup.financial_description = financial_description
        financeGroup.financial_group_class = financial_group_class
        financeGroup.financial_group_status = status
        financeGroup.save()
        return redirect('financial_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update the financial group in the database"
        context = {'error_msg':error_msg}
        return redirect('financial_links', context)  # Redirect if not POST request
    
def create_new_fattachment(request):
    if request.method == 'POST':
        financial_attachments_name = request.POST.get('financial_attachments_name')
        financial_description = request.POST.get('financial_description')
        public_display = request.POST.get('inlineRadioOptions')  # Fetch the radio button value
        attachment_cso_type = request.POST.getlist('cso_types')  # Use getlist to fetch all selected checkbox values
        # Join the list into a single string
        cso_types = ', '.join(attachment_cso_type)
        new_financial_attachment = financial_attachments(
            financial_attachments_name = financial_attachments_name,
            financial_description = financial_description,
            attachment_public_display = public_display,
            attachment_cso_type = cso_types,
        )
        new_financial_attachment.save()
    else:
        error_msg="Something went wrong while trying to save a new CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('financial_links', context)
    return redirect('financial_links') 

def update_finance_attachment(request):
    if request.method == 'POST':
        financial_attachments_id = request.POST.get('financial_attachments_id')
        financial_attachments_name = request.POST.get('financial_attachments_name')
        financial_description = request.POST.get('financial_description')
        attachment_public_display = request.POST.get('attachment_public_display')  # Fetch the radio button value
        cso_types_list = request.POST.getlist('cso_types')
        # Join the list into a single string
        cso_type = ', '.join(cso_types_list)
        status = request.POST.get('status')  # Change this line to get 'status' instead of 'duration'
        attachment = get_object_or_404(financial_attachments, financial_attachments_id=financial_attachments_id)
        attachment.financial_attachments_id = financial_attachments_id
        attachment.financial_attachments_name = financial_attachments_name
        attachment.financial_description = financial_description
        attachment.attachment_public_display = attachment_public_display
        attachment.attachment_cso_type = cso_type
        attachment.attachment_status = status
        attachment.save()
        return redirect('financial_links')  # Redirect after successful update
    else:
        error_msg="Something went wrong while trying to update the CSO in the database"
        context = {'error_msg':error_msg}
        return redirect('financial_links', context)  # Redirect if not POST request
    
def delete_financial_attachment(request, financial_attachments_id):
    financialAttachment = get_object_or_404(financial_attachments, financial_attachments_id=financial_attachments_id)
    if request.method == 'POST':
        financialAttachment.delete()
    return redirect('financial_links')  # Redirect to the master data page after deletion

def publish_post(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    posts = post_publish.objects.all()
    posts.view += 1 
    posts.save()
    context = {'role':role, 'notifications_list':notifications_list, 'posts':posts}
    return render(request, 'cso_app/administrator/manage_website/publish_post.html', context)

def post_form_upload(request):
    if request.method == 'POST':
        post_title = request.POST.get('post_title')
        post_date = request.POST.get('post_date')
        post_tag = request.POST.get('post_tag')
        featured_post = request.POST.get('featured_post')
        post_content = request.POST.get('post_content')
        post_img = request.FILES.get('post_img')

        try:
            user_id = request.user.user_id  # Fetch the user ID
            user = get_object_or_404(users, user_id=user_id)
            role = user.role
            
            # Create new post
            new_post = post_publish(
                post_id = uuid.uuid4(),
                post_img=post_img,
                post_header=post_title,
                activity=post_tag,
                status='Published',
                published_date=post_date,
                post_description=post_content,
                featured=featured_post
            )
            new_post.save()

            # Create new notification
            new_notification = notifications(
                notification_title="New post uploaded!",
                notification_content=f"New post titled {post_title} has been uploaded",
                notification_view="Admin",
                notification_orgs=user.organization,
                notification_genre='posts',
                author=user.full_name,
                user_role=role
            )
            new_notification.save()

            # Return a JSON response with a redirect URL
            return JsonResponse({'success': True, 'redirect_url': '/publish_post/'})
        except Exception as e:
            # Log or print the error for debugging
            print("Error creating post:", str(e))
            return JsonResponse({'success': False, 'message': str(e)})

    # Return a JSON response if the request method is not POST
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_post(request, post_id):
    post_details = get_object_or_404(post_publish, post_id=post_id)
    if request.method == 'POST':
        post_details.delete()
    return redirect('publish_post') 

def post_detail(request, post_id):
    # Fetch the post by UUID (post_id)
    post = get_object_or_404(post_publish, post_id=post_id)
    recent_post = post_publish.objects.order_by('-published_date')
    popular_posts = post_publish.objects.order_by('-views')

    # Count posts by category
    total_posts = post_publish.objects.count()
    news_count = post_publish.objects.filter(activity='News').count()
    announcement_count = post_publish.objects.filter(activity='Announcement').count()
    vacancy_count = post_publish.objects.filter(activity='Vaccancy').count()
    tender_count = post_publish.objects.filter(activity='Tender').count()
# Increment view count
    post.views += 1
    post.save()
    # Pass the post data and category counts to the template
    return render(request, 'cso_app/post_page.html', {
        'post': post,
        'total_posts': total_posts,
        'news_count': news_count,
        'announcement_count': announcement_count,
        'vacancy_count': vacancy_count,
        'tender_count': tender_count,'recent_post':recent_post, 'popular_posts':popular_posts
    })

def post_categories(request, category_name):
    if category_name == "All":
        # Get all posts if category is "All"
        posts = post_publish.objects.all()
    else:
        # Filter posts by the selected category
        posts = post_publish.objects.filter(activity=category_name)
    
    recent_post = post_publish.objects.order_by('-published_date')  # Get all posts sorted by publish_date
    popular_posts = post_publish.objects.order_by('-views')

    total_posts = posts.count()
    total_posts = post_publish.objects.count()
    news_count = post_publish.objects.filter(activity='News').count()
    announcement_count = post_publish.objects.filter(activity='Announcement').count()
    vacancy_count = post_publish.objects.filter(activity='Vaccancy').count()
    tender_count = post_publish.objects.filter(activity='Tender').count()
    # Increment view count
    # Pass the filtered posts and total count to the template
    return render(request, 'cso_app/post_categories.html', {
        'category_name': category_name,
        'posts': posts,
        'total_posts': total_posts,'news_count':news_count, 'announcement_count':announcement_count, 'vacancy_count':vacancy_count, 'tender_count':tender_count, 'recent_post':recent_post, 'popular_posts':popular_posts
    })

def update_post_form(request, id):
    if request.method == 'POST':
        try:
            post = post_publish.objects.get(id=id)
            
            # Update fields with new data from the request
            post.post_header = request.POST.get('post_title')
            post.published_date = request.POST.get('edit_post_date')
            post.activity = request.POST.get('post_tag')
            post.attachments = request.POST.get('post_attachment')
            post.post_description = request.POST.get('edit_post_content')
            post.featured = request.POST.get('featured_post')
            post.status = request.POST.get('post_status')
            print("This is the post: ", post, request.POST.get('edit_post_content'))
            # Handle file upload
            if 'post_img' in request.FILES:
                post.post_img = request.FILES['post_img']

            post.save()
            user_id = request.user.user_id  # Fetch the user ID
            user = get_object_or_404(users, user_id=user_id)
            role = user.role
            new_notification = notifications(
                notification_title = "Post updated!",
                notification_content = f"New post title {request.POST.get('post_title')} has been updated!",	
                notification_view = "Admin",
                notification_orgs = {request.POST.get('post_tag')},
                notification_genre = 'posts',
                author = user.full_name,
                user_role = role
            )
            new_notification.save()

            return JsonResponse({'success': True, 'redirect_url': '/publish_post/'})

        except post_publish.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Post not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    
def page_content(request):
    user_id = request.user.user_id  # Fetch the user ID
    user = get_object_or_404(users, user_id=user_id)
    role = user.role
    notifications_list = notifications.objects.all().order_by('-notification_created_at')
    contents = page_contents.objects.all()
    context = {'role':role, 'notifications_list':notifications_list, 'contents':contents}
    return render(request, 'cso_app/administrator/manage_website/page_content.html', context)

def content_page_upload(request):
    if request.method == 'POST':
        content_header = request.POST.get('content_header')
        website_page = request.POST.get('website_page')
        display_header = request.POST.get('display_header')
        page_content = request.POST.get('page_content')
        content_img = request.FILES.get('content_img')

        try:
            user_id = request.user.user_id  # Fetch the user ID
            user = get_object_or_404(users, user_id=user_id)
            role = user.role
            new_content = page_contents(
                content_header=content_header,
                display_header=display_header,
                page_content=page_content,
                website_page = website_page,
                content_img=content_img
            )
            new_content.save()
            new_notification = notifications(
                notification_title = "New post uploaded!",
                notification_content = f"New page content header: {content_header} has been uploaded",
                notification_view = "Admin",
                notification_orgs = user.organization,
                notification_genre = 'posts',
                author = user.full_name,
                user_role = role
            )
            new_notification.save()
            # Return a JSON response with a redirect URL
            return JsonResponse({'success': True, 'redirect_url': '/page_content/'})
        except Exception as e:
            # Return a JSON response with an error message
            return JsonResponse({'success': False, 'message': str(e)})

    # Return a JSON response if the request method is not POST
    return JsonResponse({'success': False, 'message': 'Invalid request method'})