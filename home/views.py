from email import message
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.http import HttpResponseRedirect

from django.contrib.auth.models import Group

# Create your views here.

def notification():
    status = Status.objects.get(status='pending')
    new = Tutor.objects.filter(status=status)
    count = 0
    for i in new:
        count += 1
    d = {'count': count, 'new': new}
    return d


def error(request):
    return render(request, 'error.html')

    

def home(request):
    subjects = Subject.objects.all()
    
    context = {'subjects': subjects}
    return render(request, 'index.html', context)

def about(request):
    users = Tutor.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'about.html', context)

def contact(request):
    
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        content = request.POST.get('desc')

        
        if name != "" and email != "" and phone != "" and content != "":
            mycontact = Contact(name=name, email=email, phone=phone,
                                address=address, content=content)
            mycontact.save()
            messages.success(request, 'Thank You For submitting form. We will reach you ASAP!!')

        else:
            messages.error(request, 'Please Fill Up the Form Correctly!!')

    return render(request, 'index.html')

def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects': subjects})

def search(request):
    page = True
    query = request.GET.get('search')
    
    if len(query) > 50:
        subject = Subject.objects.none()

    else:
        allSubTitle = Subject.objects.filter(sub_name__icontains=query)
        allSubdesc = Subject.objects.filter(sub_desc__icontains=query)
        subject = allSubTitle.union(allSubdesc)

    
    context = {'subject': subject, 'query': query, 'page': page}
    return render(request, 'search.html', context)



# View subjects and related tutors
def subView(request, pk):
    sub = Subject.objects.get(sub_id=pk)
    users = Tutor.objects.filter(subject=sub)
    count = users.count()
    print(request.user)
    subjects = Subject.objects.all().exclude(sub_id=pk)

    return render(request, 'subview.html', {'sub':sub, 'subjects':subjects, 'users':users, 'count': count})


# Login Authentication
# Tutor registration
def registeruser(request):
    page = 'user_register'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    subjects = Subject.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        cert = request.FILES.get('cert')
        
        # Create the user
        if User.objects.filter(username = data['user_username']).exists():
            messages.error(request, 'Username Already Exists.')
        
        elif User.objects.filter(email=data['user_email']).exists():
            messages.error(request, 'Email Already Exists.')
        
        elif data['user_pass1'] != data['user_pass2']:
            messages.error(request, 'Passwords donot match with each other!!')
        
        else:
            user = User.objects.create_user(username=data['user_username'].lower(), email=data['user_email'], password=data['user_pass1'], first_name=data['user_fname'], last_name=data['user_lname'])
            user.save()

            my_group = Group.objects.get(name='tutor') 
            my_group.user_set.add(user)

            subject = Subject.objects.get(sub_id=data['subject'])

            stat = Status.objects.get(status='pending')
            Tutor.objects.create(user=user, image=image, cert=cert, phone=data['user_phone'], address=data['user_address'],qualification=data['qual'], subject=subject , experience=data['exp'], status=stat)
            messages.success(request, 'Your user account has been created!! Please Login!')
            return redirect('login')
            
    context = {'page': page, 'subjects':subjects}
    return render(request, 'login_register.html', context)


# Customer or Student Register page
def customer_register(request):
    page = 'customer_register'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('c_image')

        # Create the user
        if User.objects.filter(username=data['customer_username']).exists():
            messages.error(request, 'Username Already Exists.')

        elif User.objects.filter(email=data['customer_email']).exists():
            messages.error(request, 'Email Already Exists.')

        elif data['customer_pass1'] != data['customer_pass2']:
            messages.error(request, 'Passwords donot match with each other!!')
        
        else:
            customer = User.objects.create_user(
                data['customer_username'].lower(), data['customer_email'], data['customer_pass1'], first_name=data['customer_fname'], last_name=data['customer_lname'])
            customer.save()
            my_group = Group.objects.get(name='customer') 
            my_group.user_set.add(customer)
            Customer.objects.create(user=customer,  image=image,
                                    phone=data['customer_phone'], address=data['customer_address'])
            messages.success(request, 'Your user account has been created!! Please Login!')
            return redirect('login')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def handleLogin(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!!')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('loginusername')
        password = request.POST.get('loginpass')

        user = authenticate(request, username=username, password=password)
        sign = ''

        if user is not None:
            try:
                sign = Customer.objects.get(user=user)
            except:
                pass
            
            if sign:
                login(request, user)
                messages.success(request, 'User login successfully!')
                return redirect('home')
            
            else:
                stat = Status.objects.get(status = 'accept')
                ser = False
                try:
                    ser = Tutor.objects.get(status= stat, user=user)
                
                except:
                    pass
                
                if ser:
                    login(request, user)
                    messages.success(request, 'User login successfully!')
                    return redirect('home')
                
                else:
                    messages.error(request, 'Either your request is pending or you arenot a Member')
                    return redirect('login')
        else:
            messages.error(
                request, 'Username and password does not match!! Please enter right credential!')
            return redirect('login')
        
    context = {'page': page}
    return render(request, 'login_register.html', context)

@login_required(login_url='login')
def handleLogout(request):
    logout(request)
    messages.success(request, 'User logout successfully!')
    return redirect('home')




def admin_login(request):
    page = 'admin_login'
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!!')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('logusername')
        password = request.POST.get('logpass')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('error')
        
        else:
            messages.error(
                request, 'Username and password does not match!! Please enter right credential!')
            return redirect('login')
    else:
        context = {'page': page}
        return render(request, 'login_register.html', context)
        
# profile
@login_required(login_url='login')
def profile(request):
    users = User.objects.get(id=request.user.id)

    try:
        page = False
        profile = Customer.objects.get(user=users)

    except:
        page = True
        profile = Tutor.objects.get(user=users)

    return render(request, 'profile.html', {'profile': profile, 'page': page})



# Booking
def booking(request, pid):
    if not request.user.is_authenticated:
        messages.error(request, "You must login to book a tutor.")
        return redirect('login')
    
    try:
        customer = Customer.objects.get(user=request.user)
    except:
        messages.error(request, "You must be a customer to book a tutor! You can just contact through mail.")
        return redirect('subjects')
    
    u = User.objects.get(id=pid)
    tutor = Tutor.objects.get(user=u)

    if request.method == "POST":
        data = request.POST
        status = Status.objects.get(status="pending")
        book = Booking.objects.create(status=status, user=tutor, customer=customer, grade=data['message'], book_days=data['day'], book_hours=data['hour'])
        messages.success(request, "The Teacher has been notified about your booking!!!")
        return redirect('booking_details')
    
    return render(request, 'booking.html', {'tutor': tutor, 'customer': customer})


def bookingDetails(request):
    page = True
    user = User.objects.get(id=request.user.id)
    try:
        customer = Customer.objects.get(user=user)
        books = Booking.objects.filter(customer=customer)

    except:
        return redirect('user_booking')

    context = {'books': books, 'page': page}
    return render(request, 'booking_details.html', context)


# Customer Cancellation View
@login_required(login_url='login')
def cancelBooking(request, pid):
    ser = Booking.objects.get(id=pid)
    ser.delete()
    return redirect('booking_details')

# Service Provider Details
@login_required(login_url='login')
def bookingStatus(request, pid):
    book = Booking.objects.get(id=pid)
    
    return render(request, 'booking_status.html', {'book': book})

# Accept Confirmation
@login_required(login_url='login')
def accept_confirmation(request, pid):
    ser = Booking.objects.get(id=pid)
    sta = Status.objects.get(status='accept')
    ser.status = sta
    ser.save()
    return redirect('booking_details')


# Tutor Cancelling Booking
@login_required(login_url='login')
def spcancelBooking(request, pid):
    ser = Booking.objects.get(id=pid)
    sta = Status.objects.get(status='reject')
    ser.status = sta
    ser.save()
    return redirect('booking_details')

    

# Admin Panel
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_staff:
        dic = notification()
        subjects = Subject.objects.all().count()
        users = Tutor.objects.all().count()
        customers = Customer.objects.all().count()

        status = Status.objects.get(status='pending')
        new = Tutor.objects.filter(status=status)
        count=0
        for i in new:
            count+=1
        
        cus = Customer.objects.all()
        ser = Tutor.objects.all()
        cat = Subject.objects.all()
        count1=0
        count2=0
        count3=0
        for i in cus:
            count1+=1
        for i in ser:
            count2+=1
        for i in cat:
            count3+=1
            
        context = {'count':dic['count'],'new':dic['new'], 'customer':count1, 'tutor':count2, 'subject':count3, 'subjects': subjects, 'users': users, 'customers': customers}
        return render(request,'admin/dashboard.html',context)
    
    else:
        return redirect('home')

@login_required(login_url='login')
def allCustomers(request):
    if not request.user.is_staff:
        return redirect('error')

    customers = Customer.objects.all()

    return render(request, 'admin/allcustomers.html', {'customers': customers})


@login_required(login_url='login')
def deleteCustomer(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    customer = Customer.objects.get(id=myid)
    user = User.objects.get(username=customer)

    # To delete customer
    customer.delete()
    
    # To delete user
    user.delete()

    messages.success(request, 'Customer Deleted!')
    return redirect('allcustomers')



@login_required(login_url='login')
def allUsers(request):
    if not request.user.is_staff:
        return redirect('error')

    users = Tutor.objects.all().order_by('-status')
    
    return render(request, 'admin/allusers.html', {'users': users})

@login_required(login_url='login')
def deleteUser(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    users = Tutor.objects.get(id=myid)
    user = User.objects.get(username=users)

    # To delete Tutor
    users.delete()

    # To delete user
    user.delete()
    messages.success(request, f'{user} Deleted')
    return redirect('allusers')

@login_required(login_url='login')
def acceptUser(request, myid):
    if not request.user.is_staff:
        return redirect('error')
    
    user = Tutor.objects.get(id=myid)
    
    stat = Status.objects.get(status='accept')

    user.status = stat
    user.save()
    return redirect('allusers')

    



@login_required(login_url='login')
def allSubjects(request):
    if not request.user.is_staff:
        return redirect('error')

    subjects = Subject.objects.all()
    return render(request, 'admin/allsubjects.html', {'subjects': subjects})


@login_required(login_url='login')
def editSubjects(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    sub = Subject.objects.get(sub_id=pid)

    if request.method == 'POST':
        data = request.POST
        sub.sub_name = data['sub_name']
        sub.sub_desc = data['sub_desc']
        sub.save()

        messages.success(request, 'Subject Updated!!')

    return render(request, 'admin/edit_subject.html', {'sub': sub})


@login_required(login_url='login')
def addSubject(request):
    if not request.user.is_staff:
        return redirect('error')

    if request.method == 'POST':
        data = request.POST

        if Subject.objects.filter(sub_name=data['sub_name']).exists():
            print('Subject Already Exists.')

        else:
            subject = Subject.objects.create(
                sub_name=data['sub_name'],
                sub_desc=data['sub_desc'],
            )
            messages.success(request, 'Subject Added!!')
            return redirect('allsubjects')

    return render(request, 'add_subject.html')






@login_required(login_url='login')
def deleteSubject(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    subject = Subject.objects.get(sub_id=myid)
    print(subject.sub_name)

    subject.delete()
    messages.success(request, 'Subject Deleted!')
    return redirect('allsubjects')

# Teacher Booking Details
@login_required(login_url='login')
def userBooking(request):
    page = False
    user = User.objects.get(id=request.user.id)
    try:
        tutor = Tutor.objects.get(user=user)
        books = Booking.objects.filter(user=tutor)

    except:
        return redirect('user_booking')

    context = {'books': books, 'page': page}
    return render(request, 'booking_details.html', context)

# Admin Booking Details
@login_required(login_url='login')
def adminBooking(request):
    if not request.user.is_staff:
        return redirect('error')

    books = Booking.objects.all()
    return render(request, 'admin/admin_booking.html', {'books': books})

# Admin Feedback Details
@login_required(login_url='login')
def feedback(request):
    if not request.user.is_staff:
        return redirect('error')

    msg = Contact.objects.all()

    return render(request, 'admin/feedback.html', {'msg': msg})

# Delete Feedback
@login_required(login_url='login')
def deleteFeedback(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    msg = Contact.objects.get(id=myid)
    msg.delete()
    
    messages.success(request, 'Feedback deleted successfully!')

    return redirect('feedback')

# Admin Profile Edit and Change password

@login_required(login_url='login')
def adminProfile(request):

    if request.user.is_staff:
        user = request.user
        profile = User.objects.get(username=user)
        print(profile)
    return render(request, 'admin/admin_profile.html', {'profile': profile})


@login_required(login_url='login')
def editAdmin(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    user = User.objects.get(username=request.user)
    edit = 'profile'
    if request.method == 'POST':
        username = request.POST['admin_username']
        email = request.POST['admin_email']
        fname = request.POST['a_fname']
        lname = request.POST['a_lname']

        user.username = username
        user.email = email
        user.first_name = fname
        user.last_name = lname
        # print(user.username, user.email, user.first_name, user.last_name)
        user.save()
        messages.info(request, 'Profile Updated!')
        return redirect('admin_profile')

    return render(request, 'admin/edit_admin.html', {'user': user, 'edit': edit})


@login_required(login_url='login')
def changeAdminpass(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    user = User.objects.get(username=request.user)
    edit = 'pass'
    if request.method == 'POST':
        old_password = request.POST['pw']
        new_password = request.POST['pw1']
        again_password = request.POST['pw2']

        if user.check_password(old_password) == True:  # Check the old password
            if new_password == again_password:
                user.set_password(new_password)  # Change the new password
                user.save()
                messages.success(
                    request, 'Password changed successfully! Please Login Again!!')
                return redirect('home')
        else:
            messages.error(request, "Password donot match!!")
            return HttpResponseRedirect("")

    return render(request, 'admin/edit_admin.html', {'user': user, 'edit': edit})
