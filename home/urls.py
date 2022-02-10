from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('subjects', views.subjects, name='subjects'),
    path('subjects/<pk>', views.subView, name='subview'),
    path('add_subject/', views.addSubject, name='add_subject'),
    
    path('search/', views.search, name="seach"),
    path('contact', views.contact, name="contact"),
    
    path('profile', views.profile, name="profile"),
    
    # Register and Login
    path('login/', views.handleLogin, name='login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    

    path('user_register/', views.registeruser, name='user_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('logout/', views.handleLogout, name='logout'),
    
    path('register', views.registeruser, name='register'),
    
    
    # Booking
    path('booking/<int:pid>', views.booking, name='booking'),
    path('booking_details/', views.bookingDetails, name='booking_details'),
    path('user_booking/', views.userBooking, name='user_booking'),
    path('accept_confirmation/<int:pid>', views.accept_confirmation, name='accept_confirmation'),
    
    # Customer Cancellation
    path('cancel_booking/<int:pid>', views.cancelBooking, name= 'cancel_booking'),
    
    # Tutor Cancellations
    path('spcancel_booking/<int:pid>', views.spcancelBooking, name= 'spcancel_booking'),
    
    path('booking_status/<int:pid>', views.bookingStatus, name= 'booking_status'),



    # Admin Panel
    # path('admin_home/', views.admin_home, name= 'admin_home'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('all_subjects/', views.allSubjects, name= 'allsubjects'),
    path('all_users/', views.allUsers, name= 'allusers'),
    path('all_customers/', views.allCustomers, name= 'allcustomers'),
    path('admin_booking/', views.adminBooking, name= 'admin_booking'),
    path('feedback/', views.feedback, name='feedback'),
    path('deleteFeedback/<int:myid>', views.deleteFeedback, name= 'deleteFeedback'),


    path('admin_profile/', views.adminProfile, name= 'admin_profile'),
    path('edit_admin/<int:pid>', views.editAdmin, name= 'edit_admin'),
    path('changeadminpass/<int:pid>', views.changeAdminpass, name= 'changeadminpass'),

    # CRUD function
    
    path('editsubjects/<int:pid>', views.editSubjects, name= 'editsubjects'),
    path('deleteSubject/<int:myid>', views.deleteSubject, name='deleteSubject'),
    path('deleteCustomer/<int:myid>', views.deleteCustomer, name='deleteCustomer'),
    path('deleteUser/<int:myid>', views.deleteUser, name='deleteUser'),
    
    path('acceptUser/<int:myid>', views.acceptUser, name='acceptUser'),
    
        
    path('error/', views.error, name='error'),

    
]