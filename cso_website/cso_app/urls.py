from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test-404/', views.custom_404),  # This is for testing the 404 page

    path('cso_authority/', views.cso_authority, name='cso_authority'),
    path('vision_mission/', views.vision_mission, name='vision_mission'),
    path('organogram/', views.organogram, name='organogram'),
    #whoiswho
    path('composition_of_authority/', views.composition, name='composition_of_authority'),
    path('authority_members/', views.authority_members, name='authority_members'),
    path('cso_staff/', views.cso_staff, name='cso_staff'),
    #Registered_CSOs
    path('pbos/', views.pbos, name='pbos'),
    path('home_cso_detail/<int:cso_id>/', views.home_cso_detail, name='home_cso_detail'),
    path('mbos/', views.mbos, name='mbos'),
    path('foreign_cso/', views.foreign_cso, name='foreign_cso'),
    path('thematic/', views.thematic, name='thematic'),
    #News
    path('news/', views.news, name='news'),
    #Contact_Us
    path('contact_us/', views.contact_us, name='contact_us'),
    #Contact_Us
    path('feedback/', views.feedback, name='feedback'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('feedback_table/', views.feedback_table, name='feedback_table'),
    ##Downloads url
    path('cso_act_2007/', views.cso_act_2007, name='cso_act_2007'),
    path('publications/', views.publications, name='publications'),
    path('downloads_forms/', views.downloads_forms, name='downloads_forms'),

    #Sign_In
    path('sign_in/', views.sign_in, name='sign_in'),

    #CSO_Admin PayFees Paths
    path('cso_admin_pay_fees/', views.cso_admin_pay_fees, name='cso_admin_pay_fees'),
    path('cso_admin_renewal/', views.cso_admin_renewal, name='cso_admin_renewal'),
    path('cso_admin_pay_fees_form/', views.cso_admin_pay_fees_form, name='cso_admin_pay_fees_form'),
    path('registered_users_cso_admin/', views.registered_users_cso_admin, name='registered_users_cso_admin'),
    path('cso_add_new_user/', views.cso_add_new_user, name='cso_add_new_user'),
    path('application_status/', views.application_status, name='application_status'),
    path('cso_annual_report/', views.cso_annual_report, name='cso_annual_report'),
    path('submit_annual_report/', views.submit_annual_report, name='submit_annual_report'),


    path('pay_fees/', views.pay_fees, name='pay_fees'),
    path('recieve_payment_details/', views.recieve_payment_details, name='recieve_payment_details'),
    path('validate-info/', views.validate_info, name='validate_info'),
    path('pay_fees_form/', views.pay_fees_form, name='pay_fees_form'),
    path('pay_fees_attachment/', views.pay_fees_attachment, name='pay_fees_attachment'),
    path('fetch-payment-details/', views.fetch_payment_details, name='fetch_payment_details'),
    path('update-payment-details/', views.update_payment_details, name='update_payment_details'),
    #Sign_Out
    path('sign_out/', views.sign_out, name='sign_out'),
    #administrator
    path('administrator/', views.administrator, name='administrator'),
    path('attachment_history/', views.attachment_history, name='attachment_history'),
    path('delete_attachment_fees/<uuid:attachment_id>/', views.delete_attachment_fees, name='delete_attachment_fees'),
    path('registered_users/', views.registered_users, name='registered_users'),
    path('check_cid/', views.check_cid, name='check_cid'),
    path('add_new_user/', views.add_new_user, name='add_new_user'),
    path('delete_user/<uuid:id>/', views.delete_user, name='delete_user'),
    path('master_data/', views.master_data, name='master_data'),
    path('user_details/<uuid:user_id>/', views.user_details, name='user_details'),    
    path('user_settings/<uuid:user_id>/', views.user_settings, name='user_settings'),
    path('update_profile/<uuid:user_id>/', views.update_profile, name='update_profile'),
    path('create_new_process/', views.create_new_process, name='create_new_process'),
    path('delete-process/<int:process_id>/', views.delete_process, name='delete_process'),
    path('update_process/', views.update_process, name='update_process'),
    path('update_gewog/', views.update_gewog, name='update_gewog'),
    path('delete_gewog/<int:gewog_id>/', views.delete_gewog, name='delete_gewog'),
    path('update_dzongkhag/', views.update_dzongkhag, name='update_dzongkhag'),
    path('delete_dzongkhag/<int:dzongkhag_id>/', views.delete_dzongkhag, name='delete_dzongkhag'),
    #login_history
    path('login_history/', views.login_history, name='login_history'),
    #audit_trials
    path('audit_trials/', views.audit_trials, name='audit_trials'),
    #CSO_Master
    #cso_types
    path('cso_master_links/', views.cso_master_links, name='cso_master_links'),

    path('cso_ranks/', views.cso_ranks, name='cso_ranks'),
    path('save_cso_rank/', views.save_cso_rank, name='save_cso_rank'),
    path('cso_ranks_home/', views.cso_ranks_home, name='cso_ranks_home'),

    path('create_new_cso/', views.create_new_cso_type, name='create_new_cso'),
    path('delete-cso/<int:cso_id>/', views.delete_cso, name='delete_cso'),
    path('update_cso/', views.update_cso, name='update_cso'),
    path('create_new_thematic_cso/', views.create_new_thematic_cso, name='create_new_thematic_cso'),
    path('delete-cso-thematic/<int:cso_id>/', views.delete_thematic_cso, name='delete_thematic_cso'),
    path('update_thematic_cso/', views.update_thematic_cso, name='update_thematic_cso'),
    path('create_new_attachment/', views.create_new_attachment, name='create_new_attachment'),
    path('delete-attachment/<int:cso_attachment_id>/', views.delete_attachment, name='delete_attachment'),
    path('update_cso_attachment/', views.update_cso_attachment, name='update_cso_attachment'),
    path('create_new_cso_closing/', views.create_new_cso_closing, name='create_new_cso_closing'),
    path('delete-closing-type/<int:cso_closing_id>/', views.delete_closing_type, name='delete_closing_type'),
    path('update_closing_type/', views.update_closing_type, name='update_closing_type'),

    #Public Collection Certificate Applications url
    path('certificate/collectionlist/', views.certificate_collection, name='certificate/collectionlist/'),
    path('upload_certificate/<int:application_id>/', views.upload_certificate_application, name='upload_certificate_application'),
    path('cso_list/', views.cso_list, name='cso_list'),
    path('update_trustees/<int:cso_id>/', views.update_trustees, name='update_trustees'),
    path('cso_detail/<int:id>/', views.cso_detail, name='cso_detail'),
    path('update_pbos/', views.update_pbos, name='update_pbos'),
    path('update_mbos/', views.update_mbos, name='update_mbos'),
    path('delete_cso_list/<int:cso_id>/', views.delete_cso_list, name='delete_cso_list'),

    #Manage CSO Details
    path('creating_new_cso/', views.creating_new_cso, name='creating_new_cso'),
    path('check_cso_name/', views.check_cso_name, name='check_cso_name'),
    path('generate_certificate/', views.generate_certificate, name='generate_certificate'),

    path('creating_new_cso_form/', views.creating_new_cso_form, name='creating_new_cso_form'),

    #Annual Report Master
    path('financial_links/', views.financial_links, name='financial_links'),
    path('update_financial_class/', views.update_financial_class, name='update_financial_class'),
    path('create_new_financial_group/', views.create_new_financial_group, name='create_new_financial_group'),
    path('delete-financial-group/<int:financial_group_id>/', views.delete_financial_group, name='delete_financial_group'),
    path('update_financial_group/', views.update_financial_group, name='update_financial_group'),
    path('create_new_fattachment/', views.create_new_fattachment, name='create_new_fattachment'),
    path('update_finance_attachment/', views.update_finance_attachment, name='update_finance_attachment'),
    path('delete-financial-attachment/<int:financial_attachments_id>/', views.delete_financial_attachment, name='delete_financial_attachment'),
    path('publish_post/', views.publish_post, name='publish_post'),
    path('post_form_upload/', views.post_form_upload, name='post_form_upload'),
    path('update_post_form/<int:id>/', views.update_post_form, name='update_post_form'),
    path('page_content/', views.page_content, name='page_content'),
    path('delete_post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path('content_page_upload/', views.content_page_upload, name='content_page_upload'),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),

    path('categories/<str:category_name>/', views.post_categories, name='post_categories'),

]
