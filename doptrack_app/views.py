'''
Created on 3 feb. 2016

@author: richardberg
'''
import requests
import sys
import time

import datetime
# from datetime import datetime, timedelta
from time import mktime
import collections
import re

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
#from operator import pos

from django.core.urlresolvers import reverse
from django.template.defaulttags import register
from django.forms.forms import NON_FIELD_ERRORS

from django import http
from django.views.generic.base import View, ContextMixin
from django.template import Context, loader
from django import forms

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext 

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin       # twee methoden om permissions te testen
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError, transaction
from django.db.models import Min, Max, Prefetch, Q
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import connection

from cms.models.pagemodel import Page

from doptrack.settings import DEBUG
from doptrack_app.forms import LoginForm, ImageGaleryForm, CourseForm, BaseStudentFormSet, StudentForm, ServerControlForm, FilesForm, RequestForm 
from doptrack_app.models import Course, TimeSlot, CourseStudent
from doptrack_app.logic import getTimslots, isRecordingInTimeslot, getEndCurrentRecording, handleStudentFile
from doptrack_app.remote import RemoteServer, RemoteControl

#DATE_FORMAT = "%Y%m%d%H%M"            # yml format:   yyyymmddhhmm    
DATE_FORMAT = "%Y-%m-%d %H:%M"         # human format: yyyy-mm-dd hh:mm



@register.filter
def get_item(col, key):
    ''' Als het een dictionary is haal dan het gevraagde item eruit. '''
    if isinstance(col, dict):
        return col.get(key)
    elif isinstance(col, list):
        pass
    
@register.filter(name='has_group')
def has_group(user, group_name):
    #group = Group.objects.get(name=group_name)
    #return True if group in user.groups.all() else False
    return True if group_name in [x.name for x in user.groups.all()] else False

@register.filter
def menu(user):
    ''' bepaal sitetree menu dat gebruikt moet worden voor deze gebruiker.'''
    if user.is_authenticated():
        groupNames = [x.name for x in user.groups.all()]
        if 'student' in groupNames:
            return "student"
        if any(name in ['docent','superuser'] for name in groupNames):
            return "docent"
        if user.is_staff:
            return "admin"      # om op main pagina de documentatie van admin te kunnen plaatsen    

    return "anonymous"

@register.filter
def getCmsPageIdTemplate(request):
    # stel  cmsPageId samen op de volgende manier:  cms_<group>_<functionality>
    #      group is momenteel de treesite voor docenten en superuser is dit 
    reverseId = "cms_" + menu(request.user) + "_" + request.resolver_match.url_name
    if Page.objects.filter(reverse_id=reverseId).count() > 0:
        if DEBUG: print "CMS page found: ", reverseId 
        return reverseId                                   # toon deze cms pagina
    
    if DEBUG: print "CMS page MISSING: ", reverseId
    return None

#def getCmsPageId(user, cmsPageid):
#    reverseId = "cms_" + menu(user) + "_" + cmsPageid 
#    if Page.objects.filter(reverse_id=reverseId).count() > 0:
#        return reverseId
#    return None

@register.filter
def pp_filesize(size):
    suffix = 'B'
    try:
        num = int(size)
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Yi', suffix)
    except:
        return str(size)


class AxisData():
    ''' bedoeld voor gebruik in template.html zodat je eenvoudig    time.pk  kunt gebruiken '''
    pk = None
    val = None

    def __init__(self, pk, val):
        self.pk = pk
        self.val = val


# ________________________________ helpers
def createDayId(day):
    return day.strftime("%Y%m%d")


def createTimeId(time):
    return time.strftime("%H%M")


# ________________________________ operations
def main(request):
    return render(request, 'main.html')

def anonymousRequest(request):

    form = RequestForm(initial={'body': 'Dear doptrack admin\n\nMy name is .... \n\nI would like to make a recording.\n     the name of the satelite is: .....\n     noradid of satelite is: .....\n     start recording on: .....\n     length of recording in seconds: .....\n     and frequency of recording: .....\n\nI am going to use this data for .......\n\nOr give me an account for this website so i can schedule this recording myself\n\nTHIS IS AN SAMPLE MODIFY THIS TEXT TO WHATEVER YOU WANT TO ASK'})
         
    if request.POST:
        
        form = RequestForm(request.POST)
        
        replyEmail = form.data['replyEmail']
        body = form.data['body']
        
        try:
            validate_email(replyEmail)
        except ValidationError as e:
            print form.add_error("replyEmail", 'email address invalid')
        
        if form.is_valid():
            # get superusers emailaddresses
            superusers = User.objects.filter(groups__name='superuser')
            emailAddresses = ", ".join([x.email for x in superusers])
            
            # Als er geen superusers zijn dan een error weergeven
            if not emailAddresses: 
                messages.error(request, "No superuser email addresses found to send request to")
            else:              
                
                # Send email to all superusers                
                msg = MIMEMultipart()
                msg['From'] = replyEmail
                msg['To'] = emailAddresses
                msg['Subject'] = "doptrack.lr.tudelft.nl request"
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('mailhost.tudelft.nl', 25)
                text = msg.as_string()
                server.sendmail(replyEmail, emailAddresses, text)
                
                # Also to person self (as confirmation)
                fromAddr = 'doptrack_server_noreply@tudelft.nl'            
                msg = MIMEMultipart()
                msg['From'] = fromAddr
                msg['To'] = replyEmail
                msg['Subject'] = "doptrack.lr.tudelft.nl request confirmation"
                msg.attach(MIMEText( "this was your request on website  doptrack.lr.tudelft.nl sended to the doptrack admin.\n\n" + body, 'plain'))
                
                # TODO VOG een captcha toe.   http://django-simple-captcha.readthedocs.io/en/latest/usage.html#installation ;
                
                text = msg.as_string()
                server.sendmail(fromAddr, replyEmail, text)
                
                messages.success(request, "Thanks for the request. A confirmation email is sended to to given reply address.")
                return redirect(reverse('request'))
            
    return render(request, 'anonymousRequest.html', {'form': form}, context_instance=RequestContext(request))

def login(request):
    #auth.logout(request)                        # bij access denied word je geredirect naar de login, een user heeft menu item niet en 
    form = LoginForm()
    form.next = request.GET.get('next', '')
     
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')
        form.next = request.POST.get('next', '')
        user = auth.authenticate(username=username, password=password)
        
        if user and user.is_staff and not form.next:
            form.next = '/admin'                # admin redirecten naar admin site
            
        if user is not None:
            auth.login(request, user)
            if form.next:
                return HttpResponseRedirect(form.next)
            else:
                return HttpResponseRedirect('/')
        else:
            form.add_error(NON_FIELD_ERRORS, 'Invalid credentials')
            
    # cms page 
    context = context_instance=RequestContext(request)
    #context['cmspageid'] = 'cms_student_login'
    #context['cmspageid'] = getCmsPageId(request.user, "login" )        
    return render(request, 'login.html', {'form': form}, context )

def logout(request):
    auth.logout(request)
    return redirect(reverse('main'))


class CourseListView(ListView):

    model = Course
    template_name = 'course_list.html'

    # toon voor studenten de courses waaraan ze zelf gekoppeld zijn.
    def get_queryset(self):
        base_qs = super(CourseListView, self).get_queryset()
        
        userGroupNames = [x.name for x in self.request.user.groups.all()]
        if 'student' in userGroupNames:
            return base_qs.filter(coursestudent__user=self.request.user).order_by('start')
        return base_qs.order_by('start')

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['canEditAll'] = True if "superuser" in [x.name for x in self.request.user.groups.all()] else False
        return context


@login_required
def courseDelete(request, *wargs, **kwargs):
    if request.method == 'GET':
        
        courseId = kwargs.pop('courseId', None)
        course = Course.objects.get(pk=courseId)
        allOk = True        

        # SECURITY:  superuser or docent
        groupNames = [x.name for x in request.user.groups.all()]
        if not any(name in ['docent','superuser'] for name in groupNames):
            messages.error(request, 'only superuser or docent can delete course' )
            allOk = False
        
        # SECURITY:  een docent mag alleen zijn eigen course deleten
        if "docent" in groupNames and course.docent_id == request.user.id:
            messages.error(request, 'deleting course requires superuser or course owner rights' )
            allOk = False
            
        if allOk:
            course.delete()
        
        return redirect(reverse('course-list'))


@login_required
def courseSettings(request, *wargs, **kwargs):
    """
    backend for cource form

    GET:  showing course info and related students
    POST: updating course info and related students
    """
    courseId = kwargs.pop('courseId', None)
    if courseId:
        course = Course.objects.get(pk=courseId)
        coursestudents = CourseStudent.objects.filter(course=courseId)
    else:
        course = Course()
        coursestudents = []           # ampty array so nothing happends

    # SECURITY:
    errorAdded = False
    groupNames = [x.name for x in request.user.groups.all()]
    if not course.id:
        # SECURITY:CREATE:    alleen superuser en docent mogen course aanmaken
        if not any(name in ['docent','superuser'] for name in groupNames):
            messages.error(request, 'only superuser or docent can create course' )
            errorAdded = True            
    else:
        # SECURITY:UPDATE:    alleen superuser en docent eigenaar mogen course bewerken
        allowed = "superuser" in groupNames
        if not allowed:
            allowed = True if "docent" in groupNames and course.docent_id == request.user.id else False
        if not allowed:
            messages.error(request, 'this course can only be edited by docent owner or superuser' )
            errorAdded = True

    # Create the formset, specifying the form and formset we want to use.
    StudentFormSet = formset_factory(StudentForm, formset=BaseStudentFormSet)

    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES, course=course)
        student_formset = StudentFormSet(request.POST)

        if course_form.is_valid() and student_formset.is_valid():

            # INPUT CHECK: start moet voor eind liggen
            start = course_form.cleaned_data.get('start')
            end = course_form.cleaned_data.get('end')
            if end < start:
                course_form.add_error('start', 'starttime must be before endtime')
                course_form.add_error('end', 'endtime must be after starttime')
                errorAdded = True
    
            # INPUT CHECK: courses mogen elkaar niet overlappen (anders krijg je nu problemen met dubbel uitgedeelde tijdslots)
            overlappingCourses = Course.objects.filter(Q(start__range=[start,end]) | Q(end__range=[start, end])).exclude(id=courseId)
            if overlappingCourses:
                course_form.add_error(NON_FIELD_ERRORS, 'this start and end dates gives overlap with courses: {}'.format( ', '.join([x.name for x in overlappingCourses]) ) )
                errorAdded = True            
            
            # INPUT CHECK (redundant and can miss overlap, but when activated gives extra details about how to fix overlap)
            maximumEndTime = Course.objects.filter(end__gt=end).exclude(id=courseId).aggregate(Min('start'))['start__min']
            if maximumEndTime:
                if end >= maximumEndTime:
                    course_form.add_error('end', 'time overlaps another course. select a date smaller than {}'.format(str(maximumEndTime)) )
                    errorAdded = True 
            minimumStartTime = Course.objects.filter(start__lt=start).exclude(id=courseId).aggregate(Max('end'))['end__max']
            if minimumStartTime:
                if start <= minimumStartTime:
                    course_form.add_error('start', 'time overlaps another course. select a date bigger than {}'.format(str(minimumStartTime)) )
                    errorAdded = True
            
            #print maximumEndTime, '_____', minimumStartTime 
            #for query in connection.queries:
            #    print "SQLQUERY: ", query

            if not errorAdded:
                # prepare student data
                inputStudentData = {}
                for student_form in student_formset:
                    name = student_form.cleaned_data.get('name')
                    if name:
                        password = student_form.cleaned_data.get('password')
                        inputStudentData[name] = {'password': password}
    
                # add students from uploaded file
                if('file' in request.FILES):
                    uploadedStudents = handleStudentFile(request.FILES['file'])
                    inputStudentData.update(uploadedStudents)
    
                try:
                    with transaction.atomic():
    
                        # Save course info
                        course.name = course_form.cleaned_data.get('name')
                        course.start = course_form.cleaned_data.get('start')
                        course.end = course_form.cleaned_data.get('end')
                        course.timeslotDuration = course_form.cleaned_data.get('timeslotDuration')
                        if not course.docent_id:
                            course.docent = request.user    # niet updaten als deze al gezet is anders is superuser ineens owner
                        course.save()
    
                        currentStudentNames = []
                        for student in coursestudents:
                            username = student.user.username
                            currentStudentNames.append(username)
                            if username in inputStudentData:
                                newPassword = inputStudentData[username]['password']
                                if newPassword:
                                    # UPDATE WACHTWOORD
                                    student.user.set_password(newPassword)
                                    student.user.save()
                            else:
                                # DELETE Student
                                student.delete()
    
                        new_students = []
                        for newStudentName in inputStudentData.keys():
                            if newStudentName not in currentStudentNames:
    
                                # Ik gebruik geen get omdat die een exception geeft als het niet gevonden word.
                                userList = User.objects.filter(username=newStudentName).all()
                                if len(userList) == 1:
                                    user = userList[0]
                                else:
                                    # student bestond nog niet maak deze opnieuw aan.
                                    newPassword = inputStudentData[newStudentName]['password']
                                    user = User.objects.create_user(newStudentName, 'nvt@tudelft.nl', newPassword)      # create user
    
                                    group = Group.objects.get(name='student')
                                    user.groups.add(group)
    
                                new_students.append(user)
    
                        # INSERT StudentCourse
                        CourseStudent.objects.bulk_create(
                            [CourseStudent(user_id=x.id, course_id=course.pk) for x in new_students])
    
                        messages.success(request, 'updated course and stored related students')
                        return redirect(reverse('course-edit', kwargs={'courseId': course.id}))
    
                except IntegrityError as e:                   # If the transaction failed
                    print e
                    messages.error(request, 'There was an error saving course and students.' + str(e) )                

    else:
        # GET: fill forms with inital data.
        course_form = CourseForm(course=course)

        # laat password leeg, als het gevuld word dan moet het opnieuw gezet worden.
        studentData = [{'name': s.user.username, 'password': ''} for s in coursestudents]
        student_formset = StudentFormSet(initial=studentData)

        # ___ test
        # for s in coursestudents:
        #    print s.user.username

    context = {
        'course': course,   # treesite menu test
        'course_form': course_form,
        'student_formset': student_formset,
    }

    return render(request, 'edit_course.html', context)



class RequestTimeslotView(UserPassesTestMixin, View):
    ''' Student een timeslot laten reserveren.

        GET:    ophalen courseinfo en alle gereserveerde timeslotst
        POST:   reserveren van 1 tijdslot en als die al gereserveerd is weer verijgeven'''

    # SECURITY:  Next 2 functions are used by UserPassesTestMixin
    def test_func(self):
        if 'student' in [x.name for x in self.request.user.groups.all()]:
            return True

    def handle_no_permission(self):
        messages.error(self.request, 'ACCESS DENIED:  Log in as student')
        return super(RequestTimeslotView, self).handle_no_permission()          # login first        

    def get(self, request, *args, **kwargs):

        courseId = kwargs.pop('courseId', None)

        # SECURITY:  alleen als je bent toegevoegd aan de course als student
        if CourseStudent.objects.filter(user_id=request.user.id, course_id=courseId).count() != 1:
            messages.error(request, "Access denied: you are not a student of this course")
            return redirect(reverse('main'))

        if courseId:
            course = Course.objects.get(pk=courseId)

        # Laad de data
        gridDayAxis = []
        gridTimeStepAxis = []
        gridData = {}

        if course:
            print course

            # grid axis: day
            delta = course.end - course.start
            for day in range(delta.days+1):
                day = course.start + datetime.timedelta(days=day)
                gridDayAxis.append(AxisData(createDayId(day), day))
            print "gridDayAxe: ", gridDayAxis

            # grid axis: duration
            step = course.timeslotDuration.hour*60+course.timeslotDuration.minute
            for minutesTimeSlot in range(0, 24*60, step):
                hour, minute = divmod(minutesTimeSlot, 60)
                time = datetime.time(hour, minute, 0)
                gridTimeStepAxis.append(AxisData(createTimeId(time), time))
            print "gridTimeStepAxe: ", gridTimeStepAxis

            # gridData  (NOTE: ik hou nog geen rekening met veranderinge van course start, end en timeslot)
            courseStudentList = CourseStudent.objects.filter(course=course) \
                .select_related('user').prefetch_related('timeslot_set').all()

            for courseStudent in courseStudentList:
                cnt = 0
                for timeSlot in courseStudent.timeslot_set.all():
                    cnt = cnt + 1
                    # print timeSlot.start.date(), timeSlot.start.time(), courseStudent.student
                    pkDay = createDayId(timeSlot.start.date())
                    pkTime = createTimeId(timeSlot.start.time())

                    dayData = {}
                    if pkDay in gridData:
                        dayData = gridData[pkDay]
                    else:
                        gridData[pkDay] = dayData

                    celData = []
                    if pkTime in dayData:
                        celData = dayData[pkTime]
                    else:
                        dayData[pkTime] = celData
                        
                    pkLabel = AxisData(str(courseStudent.user_id) + "c" + str(cnt), courseStudent.user)
                    celData.append(pkLabel)

            print "gridData: ", gridData

            for query in connection.queries:
                print "SQLQUERY: ", query

        # ____ Dit werkt voor CSRF en voor non form data, Maar vraag me af of dit wel zo de bedoeling is
        #          (had gehoopt dat ContextMxin zou werken)
        context = RequestContext(request, current_app=None)
        context['course'] = course
        context['gridDayAxis'] = gridDayAxis
        context['gridTimeStepAxis'] = gridTimeStepAxis
        context['gridData'] = gridData
        context['closedTimeslotDateTime'] = datetime.datetime.now() - datetime.timedelta(minutes=step)

        #form = NameForm()
        response = render(request, 'request_timeslot.html', {'form': None}, context_instance=context)
        return response

    def post(self, request, *args, **kwargs):

        courseId = kwargs.pop('courseId', None)
        userId = request.user.id
        day = request.POST.get('day', None)
        time = request.POST.get('time', None)
        print "user: ", request.user.id
        print "day: ", day
        print "time: ", time

        # hieronder een test omdat submit een post en een get genereert.
        if not (day and time):
            return redirect(reverse('requesttimeslot', kwargs={'courseId': courseId}))

        courseStudentQuerySet = CourseStudent.objects.filter(course_id=courseId, user=request.user)
        courseStudent = courseStudentQuerySet[0]

        comp = re.compile(r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})$')
        m = comp.match(day+time)
        if m:
            stamp = datetime.datetime(*(int(m.group(x)) for x in range(1, 6)), second=0, microsecond=0)
            print stamp

        # is het een geldig slot volgens course settings. ? (Valid times) en dag conatrole  (generieke operatie maken die geldige tijden teruggeeft)

        # timeslot
        timeslotQuerySet = TimeSlot.objects.filter(start__exact=stamp)
        if len(timeslotQuerySet):
            timeslot = timeslotQuerySet[0]
            if timeslot.coursestudent.user_id == request.user.pk:
                # slot is al gereserveerd door deze student, geef het weer vrij.
                timeslot.delete()
                messages.success(request, "timeslot released")
            else:
                # slot is al gerereserveerd door andere student, niets doen
                messages.warning(request, "timeslot already taken")
        else:
            # hoeveel slots heeft deze gebruiker nu  (Nu hard gecodeerd, dus verwijderen of in course instelbaar maken)
            timeslotQuerySet = TimeSlot.objects.filter(coursestudent=courseStudent)
            if len(timeslotQuerySet) >= 2:
                messages.warning(request, "max slots exceeded")
            else:
                # slot is nog vrij, reserveer het voor deze student
                timeslot = TimeSlot(coursestudent=courseStudent, start=stamp, modified=datetime.datetime.now())
                timeslot.save()
                messages.success(request, 'timeslot reserved')

        # for query in connection.queries:
        #    print "SQLQUERY: ", query

        return redirect(reverse('requesttimeslot', kwargs={'courseId': courseId}))


#PermissionRequiredMixin
class ManageTimeslotsViewView(UserPassesTestMixin, View):
    ''' Docent timeslots aan studenten toekennen.

        GET:    ophalen courseinfo en alle gereserveerde timeslotst
        POST:   reserveren van 1 tijdslot en als die al gereserveerd is weer verijgeven'''

    # next 2 functions are used by UserPassesTestMixin
    def test_func(self):
        
        # SECUTITY:  superuser en docent.owner mogen bewerken
        groupNames = [x.name for x in self.request.user.groups.all()]
        if not any(name in ['docent','superuser'] for name in groupNames):
            messages.error(self.request, 'only superuser or docent can manage timeslots' )
            return False
        
        return True

    def handle_no_permission(self):        
        return super(ManageTimeslotsViewView, self).handle_no_permission()      # show login page and return to this after login.   

    # check here for illegal access errors.  (already logged in with correctly, so no need to go to login page)
    def illegalAccessCheck(self):    

        # INPUT VALIDATION: bestaat course 
        courseId = self.kwargs.pop('courseId', None)
        try:
            course = Course.objects.get(pk=courseId)
        except Course.DoesNotExist:
            messages.error(self.request, 'Requested course not found')
            return True
                
        # SECURITY: docenten mogen alleen eigen course bewerken.
        groupNames = [x.name for x in self.request.user.groups.all()] 
        if 'docent' in groupNames and course.docent_id != self.request.user.id:
            messages.error(self.request, "Access denied: you are not the course owner")
            return True

    def get(self, request, *args, **kwargs):
        
        if self.illegalAccessCheck():
            return redirect(reverse('main'))             
        
        courseId = kwargs.pop('courseId', None)
        course = Course.objects.get(pk=courseId)        # er is al gecontroleerd of course bestaat. 

        # Laad de data
        gridDayAxis = []
        gridTimeStepAxis = []
        gridData = {}
        students = []

        if course:
            print course

            # grid axis: day
            delta = course.end - course.start
            for day in range(delta.days+1):
                day = course.start + datetime.timedelta(days=day)
                gridDayAxis.append(AxisData(createDayId(day), day))
            print "gridDayAxe: ", gridDayAxis

            # grid axis: duration
            step = course.timeslotDuration.hour*60+course.timeslotDuration.minute
            for minutesTimeSlot in range(0, 24*60, step):
                hour, minute = divmod(minutesTimeSlot, 60)
                t = datetime.time(hour, minute, 0)
                gridTimeStepAxis.append(AxisData(createTimeId(t), t))
            print "gridTimeStepAxe: ", gridTimeStepAxis

            # gridData  (NOTE: ik hou nog geen rekening met veranderinge van course start, end en timeslot)
            courseStudentList = CourseStudent.objects.filter(course=course) \
                .select_related('user').prefetch_related('timeslot_set').all()
            for courseStudent in courseStudentList:
                students.append(courseStudent.user)
                cnt = 0
                for timeSlot in courseStudent.timeslot_set.all():
                    cnt = cnt + 1
                    # print timeSlot.start.date(), timeSlot.start.time(), courseStudent.student
                    pkDay = createDayId(timeSlot.start.date())
                    pkTime = createTimeId(timeSlot.start.time())

                    dayData = {}
                    if pkDay in gridData:
                        dayData = gridData[pkDay]
                    else:
                        gridData[pkDay] = dayData

                    celData = []
                    if pkTime in dayData:
                        celData = dayData[pkTime]
                    else:
                        dayData[pkTime] = celData

                    pkLabel = AxisData(str(courseStudent.user_id) + "c" + str(cnt), courseStudent.user)
                    celData.append(pkLabel)

            print "gridData: ", gridData

            # for query in connection.queries:
            #    print "   SQL_XXX: ", query

        # ____ Dit werkt voor CSRF en voor non form data, Maar vraag me af of dit wel zo de bedoeling is
        #          (had gehoopt dat ContextMxin zou werken)
        context = RequestContext(request, current_app=None)
        context['course'] = course              # sitetree menu
        context['students'] = students
        context['gridDayAxis'] = gridDayAxis
        context['gridTimeStepAxis'] = gridTimeStepAxis
        context['gridData'] = gridData
        
        response = render(request, 'manage_timeslots.html', {'form': None}, context_instance=context)
        return response

    def post(self, request, *args, **kwargs):

        if self.illegalAccessCheck():
            return redirect(reverse('main'))             

        courseId = kwargs.pop('courseId', None)

        # verwerk input timeslot, persoon koppelingen.
        comp = re.compile(r'^ts\[(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})\]$')
        newTimslotList = []
        for key, val in request.POST.iteritems():
            print key, val
            m = comp.match(key)
            if m:
                stamp = datetime.datetime(*(int(m.group(x)) for x in range(1, 6)), second=0, microsecond=0)
                studentId = int(val)
                newTimslotList.append((stamp, studentId))

        print "newTimslotList: ", newTimslotList

        map_StudentId_to_courseStudent = {}
        with transaction.atomic():
            # delete records that does not exist annymore
            courseStudentList = CourseStudent.objects.filter(course=courseId) \
                .select_related('user').prefetch_related('timeslot_set').all()
            for courseStudent in courseStudentList:
                map_StudentId_to_courseStudent[courseStudent.user_id] = courseStudent
                for timeSlot in courseStudent.timeslot_set.all():
                    timslotData = (timeSlot.start, courseStudent.user_id)
                    print "timslotData: ", timslotData
                    if timslotData in newTimslotList:
                        newTimslotList.remove(timslotData)  # Dit slot is nog steeds voor deze student dus:  niets doen
                    else:
                        timeSlot.delete()                   # Dit timeslot zit voor deze persoon niet meer in de input.

            # insert new records
            print newTimslotList

            for timeslotData in newTimslotList:
                studentId = timeslotData[1]
                timeslot = TimeSlot(coursestudent=map_StudentId_to_courseStudent[studentId],
                                    start=timeslotData[0],
                                    modified=datetime.datetime.now())
                timeslot.save()

        for query in connection.queries:
            print "   SQL_XXX: ", query

        return redirect(reverse('managetimeslots', kwargs={'courseId': courseId}))


class ServerControlView(View):
    """
    backend for ServerControl form

    GET:  fill in default start time.
    POST: schedule recording
    """
    def getSchedules(self, request):
        schedules = RemoteControl().getScheduleFileInfo()

        # get user timeslots
        dateFilter = datetime.datetime.now() - datetime.timedelta(hours=48)     # TODO alle tijdslots in toekomst ?
        slots = getTimslots(request.user.id, dateFilter)
    
        # __ Bepaal of gebruiker een schedule mag verwijderen
        for schedule in schedules:
            startSchedule = schedule['time']
            endSchedule = startSchedule + datetime.timedelta(seconds=int(schedule['length']))
    
            if 'userid' in schedule:
                if schedule['userid'] == request.user.id:
                    # gebruiker heeft schedule ooit aangemaakt en mag hem verwijderen.
                    #     (Mogelijk is dit niet nodig en niet gewenst)
                    schedule['canDelete'] = True
                    continue
    
                for slot in slots:
                    # Dit schedule is aangemaakt via deze webapp
                    #  , maar bevind zich nu in slot andere gebruiker, hij mag hem verwijderen.
                    if endSchedule > slot['start'] and startSchedule < slot['end']:
                        schedule['canDelete'] = True
        return schedules
    
    def get(self, request, *args, **kwargs):
        
        # default form data
        data = {'starttime': (datetime.datetime.now() + datetime.timedelta(minutes=15) ).strftime(DATE_FORMAT),
                'length': 700}
        form = ServerControlForm(initial=data)
        
        context = RequestContext(request, current_app=None)
        context['schedules'] = self.getSchedules(request)
        
        return render(request, 'server_control.html', {'form': form}, context_instance=context)

    def post(self, request, *args, **kwargs):
        
        form = ServerControlForm(request.POST)
        starttime = form.data['starttime']
        #starttime = re.sub("[^0-9]", "", starttime)    # dit gaat fout omdat formaat nu via 1 var instelbaar is. 
        length = int(form.data['length'])

        # SECURITY
        scheduleRecording = True;
        groupNames = [x.name for x in self.request.user.groups.all()]
        if not any(name in ['student','docent','superuser'] for name in groupNames):
            messages.error(self.request, "Access denied:  only for student, instructor or superuser")
            scheduleRecording = False
            
        if form.is_valid():
            
            # ______ INPUT CHECK: start time format
            try:
                start = datetime.datetime.strptime(starttime, DATE_FORMAT)
            except:
                form.add_error('starttime', 'failed to read start datetime, check the format')
                scheduleRecording = False
    
            # ______ INPUT CHECK: start kan niet in verleden zijn (5 sec safe marge)
            if (start < datetime.datetime.now()+datetime.timedelta(seconds=5)):
                form.add_error('starttime', 'starttime is in the past')
                scheduleRecording = False
    
            # ______ INPUT check if no scheduled recording is running or is starting in 10 sec
            endCurrentRecording = getEndCurrentRecording()
            if endCurrentRecording and endCurrentRecording > start:
                form.add_error('starttime', 'Currently running recording cant be stoped, and is still recording at given start time')
                scheduleRecording = False
            
            # ______ SECURITY: student mag alleen maar schedulen in je eigen slot
            if 'student' in groupNames:
                if not(isRecordingInTimeslot(request.user.id, start, length)):
                    messages.error(self.request, 'you can can only schedule a recording in your own timeslot')
                    scheduleRecording = False

            if scheduleRecording:
                # ______ no problems detected so request schedule
                try:
                    noradid = form.data['noradid'].strip()
                    frequency = form.data['frequency'].strip()
                    satellitename = form.data['satellitename'].strip()
                    remote = RemoteControl()
                    result = remote.addRecordSchedule(noradid, satellitename, length, frequency, request.user.id, start)
                    
                except:
                    e = sys.exc_info()[0]
                    result = str(e)
        
                if result == "done":
                    messages.success(self.request, 'recording request sended to server, check if it is scheduled')
                    return redirect(reverse('servercontrol', kwargs={})) 
                else:
                    messages.error(self.request, "Failed to send recording request to server: " + result)


        #return render(request, 'server_control.html', {'form': form})
        context = RequestContext(request, current_app=None)
        context['schedules'] = self.getSchedules(request)
        
        return render(request, 'server_control.html', {'form': form}, context_instance=context)



# This function is used by an ajax call
@never_cache
def serverControlActivity(request):
    
    hoursPast = int(request.GET.get('hoursPast', ''))
    hoursFuture = int(request.GET.get('hoursFuture', ''))
    starttime = request.GET.get('starttime', '')
    #starttime = re.sub("[^0-9]", "", starttime)        # als je dit doet moet het date format dat gebruikt word bij parsen ingevoerde waarde ook zonder tekens zijn.  
    length = request.GET.get('length', '') 
    satellitename = request.GET.get('satellitename', '')
    noradid = request.GET.get('noradid', '')

    feedbackList = []
    if hoursPast < 1:
        hoursPast = 1
        feedbackList.append('ignoring given past hours, using the minimum 1')
    if hoursPast > 48:
        hoursPast = 48
        feedbackList.append('ignoring given past hours, using the maximum 48')
    if hoursFuture < 1:
        hoursFuture = 1
        feedbackList.append('ignoring given coming hours, using the minimum 1')
    if hoursFuture > 90:
        hoursFuture = 90
        feedbackList.append('ignoring given coming hours, using the maximum 90')

    # doptrack.tudelft.nl server information
    remote = RemoteControl()
    schedules = remote.getScheduleFileInfo()
    recordings = remote.getRecordingFileInfo(2)

    # ____ Dit is coole techniek maar lastig met debuggen dus toch maar niet gebruiken 
    #remote = RemoteServer()
    #schedules = remote.getSchedule()
    #recordings = remote.getRecord()
    #feedbackList.extend( remote.getFeedbackList() )


    # config html control
    ctrlWidth = 600
    startPointLoc = 30

    sizeTimeline = ctrlWidth - 2 * startPointLoc
    startTime = datetime.datetime.now() - datetime.timedelta(hours=hoursPast)
    endTime = datetime.datetime.now() + datetime.timedelta(hours=hoursFuture)
    deltaTime = endTime - startTime

    ctrlData = {'width': ctrlWidth,
                'start_px': startPointLoc,
                'start_label': startTime.strftime(DATE_FORMAT) + " (-" + str(hoursPast) + "h)",
                'end_px': ctrlWidth - startPointLoc,
                'end_label': endTime.strftime(DATE_FORMAT) + " (+" + str(hoursFuture) + "h)",
                'now_px': int(startPointLoc + sizeTimeline * (((datetime.datetime.now()-startTime).total_seconds())/deltaTime.total_seconds())),
                'now_label': datetime.datetime.now().strftime(DATE_FORMAT) + " (now)",
                'nowRecording': getEndCurrentRecording(5, schedules) }

    # timeslots of students
    startDateFilterStart = datetime.datetime.now() - datetime.timedelta(hours=hoursPast)
    startDateFilterEnd = datetime.datetime.now() + datetime.timedelta(hours=hoursFuture)

    timeslotList = TimeSlot.objects.filter(start__range=(startDateFilterStart, startDateFilterEnd)) \
                        .select_related('coursestudent','coursestudent__user','coursestudent__course').order_by('start').all()
    timeslotData = []
    for ts in timeslotList:
        start = ts.start
        end = ts.start + datetime.timedelta(hours=ts.coursestudent.course.timeslotDuration.hour,
                                            minutes=ts.coursestudent.course.timeslotDuration.minute,
                                            seconds=ts.coursestudent.course.timeslotDuration.second)
        startpos = startPointLoc + sizeTimeline * (((start-startTime).total_seconds())/deltaTime.total_seconds())
        endpos = startPointLoc + sizeTimeline * (((end-startTime).total_seconds())/deltaTime.total_seconds())
        data = {}
        data['px_start'] = int(startpos)
        data['width'] = int(endpos-startpos)
        data['user'] = ts.coursestudent.user
        data['label'] = start.strftime(DATE_FORMAT) + " to " + end.strftime(DATE_FORMAT)
        # print "slot data: ", data
        if 0 <= startpos <= ctrlWidth:
            timeslotData.append(data)

    # virtual point
    try:
        startTT = time.strptime(starttime, DATE_FORMAT)  
        start = datetime.datetime.fromtimestamp(mktime(startTT))
        end = start + datetime.timedelta(seconds=int(length))
        startpos = startPointLoc + sizeTimeline * (((start-startTime).total_seconds())/deltaTime.total_seconds())
        endpos = startPointLoc + sizeTimeline * (((end-startTime).total_seconds())/deltaTime.total_seconds())
        if 0 <= startpos <= ctrlWidth:
            ctrlData['virtual_px_start'] = int(startpos)
            ctrlData['virtual_width'] = int(endpos-startpos)
            ctrlData['virtual_start'] = starttime
            ctrlData['virtual_satellitename'] = satellitename
            ctrlData['virtual_noradid'] = noradid
    except:
        ctrlData['feedback'] = "Failed to read starttime and length. unable to show the not yet scheduled recording in pink"

    # calculate scheduled locations  
    scheduledata = []
    for schedule in schedules:  # schedule = dict: {'length': 660, 'id': 'FUNcube-1_39444_201708172306', 'time': datetime.datetime(2017, 8, 17, 23, 6)}
        start = schedule['time']
        end = start + datetime.timedelta(seconds=int(schedule['length']))
        startpos = startPointLoc + sizeTimeline * (((start-startTime).total_seconds())/deltaTime.total_seconds())
        endpos = startPointLoc + sizeTimeline * (((end-startTime).total_seconds())/deltaTime.total_seconds())
        schedule['px_start'] = int(startpos)
        schedule['width'] = int(endpos-startpos)

        m = re.search('(.*)_(\w*)_(\w*)', schedule['id'])       # Delfi-C3_32789_201607122151
        if m:
            schedule['satellite_name'] = m.group(1)
            schedule['noradid'] = m.group(2)

        if 0 <= startpos <= ctrlWidth:
            scheduledata.append(schedule)

    # calculate recordings locations
    recordingData = []
    for recording in recordings:
        start = recording['time']
        end = start + datetime.timedelta(seconds=int(recording['length']))
        startpos = startPointLoc + sizeTimeline * (((start-startTime).total_seconds())/deltaTime.total_seconds())
        endpos = startPointLoc + sizeTimeline * (((end-startTime).total_seconds())/deltaTime.total_seconds())
        recording['px_start'] = int(startpos)
        recording['width'] = int(endpos-startpos)
        
        m = re.search('(.*)_(\w*)_(\w*)', recording['id'])       # Delfi-C3_32789_201607122151
        if m:
            recording['satellite_name'] = m.group(1)
            recording['noradid'] = m.group(2)
            recording['file-name'] = m.group(2)
            
        if 0 <= startpos <= ctrlWidth:
            recordingData.append(recording)

    context = RequestContext(request, current_app=None)
    context['ctrlData'] = ctrlData
    context['timeslots'] = timeslotData
    context['schedules'] = scheduledata
    context['recordings'] = recordingData
    if len(feedbackList) > 0:
        context['feedbackList'] = feedbackList

    response = render(request, 'ctrl_serveractivity.html', context_instance=context)
    return response


# weergeven recordings
def downloadFiles(request):
    days = 3

    if request.method == 'POST':
        files_form = FilesForm(request.POST)
        try:
            days = int( files_form.data['days'] )
        except:
            files_form.add_error('days', 'invalid number')
    else:
        files_form = FilesForm(initial={'days': days})

    recordings = RemoteControl().getRecordingFileInfo(days)
    context = {
        'recordings': recordings,
        'files_form': files_form,
    }

    return render(request, 'files.html', context)


def deleteSchedule(request, *wargs, **kwargs):
    fileId = kwargs['fileId']

    # SECURITY:  mag gebruiker dit schedule wel verwijderen.
    schedules = RemoteControl().getScheduleFileInfo()
    schedule = next(x for x in schedules if x['id'] == fileId)
    if schedule:
        if 'userid' in schedule:
            canDelete = False

            # Dit schedule is aangemaakt via deze webapp
            if schedule['userid'] == request.user.id:
                # deze user is owner of deze schedule
                canDelete = True
            else:
                startSchedule = schedule['time']
                endSchedule = startSchedule + datetime.timedelta(seconds=int(schedule['length']))

                dateFilter = datetime.datetime.now() - datetime.timedelta(hours=24)
                slots = getTimslots(request.user.id, dateFilter)
                for slot in slots:
                    #  , maar bevind zich nu in slot andere gebruiker, hij mag hem verwijderen.
                    if endSchedule > slot['start'] and startSchedule < slot['end']:
                        canDelete = True

            if canDelete:
                RemoteControl().deleteSchedule(fileId)
                messages.success(request, 'delete commando sended to server')
            else:
                messages.error(request, 'you can only remove user schedules if they are in your slot or if you created it.')
        else:
            messages.error(request, 'This schedule is owned by the server. When it confilcts with an user schedule it removed automatic')
    else:
        messages.error(request, 'Schedule to delete not found')

    #return redirect('downloadFiles')
    return redirect(reverse('servercontrol', kwargs={}))


def zipRecording(request, *wargs, **kwargs):
    RemoteControl().zipRecording(kwargs['fileId'])
    messages.success(request, "The recording is being zipped by the server and placed in a download folder (this will take about 2 minutes). We recommend you take a break and return to this page when the download is ready and a download link is shown.")
                                   
    return redirect('downloadFiles')


#   http://127.0.0.1:8000/images/Delfi-C3_32789_201803182039/#&gid=1&pid=Delfi-C3_32789_201803182039
def imageGallery(request, *wargs, **kwargs):

    # default    
    startLoc=1
    endLoc = defaultImageCollectionSize = 20

    # eventueel opgevraagde picture       
    pid = kwargs.pop('pid', None)
    
    if request.method == 'POST':
        form = ImageGaleryForm(request.POST)
        startLoc = int(form.data['min'])
        endLoc = int(form.data['max'])
        
        if startLoc > endLoc:
            form.add_error(NON_FIELD_ERRORS, "This doesn't work, try to switch the numbers" )

    imageData = None

    # Als een specifieke image gehaald word, dan zorgen dat image in collectie zit
    if pid and pid!='pid':
        
        # Haal alle image gegevens op, je weet niet waar image zit. (1e keer 10 sec, daarna 1 uur in cache.)   
        imageData = RemoteControl().getImageFileInfo(None, None, None)
    
        # bepaal locatie van de image
        pos = next( (i for i, item in enumerate(imageData) if item['id'] == pid), None )
        if pos == None:
            messages.error(request, 'requested image not found')
        else:
            # bepaal welke elementen teruggegeven gaan worden zodat gevraagde image er in zit
            if pos >= endLoc:
                startLoc = pos - defaultImageCollectionSize/2 + 1
                endLoc = pos + defaultImageCollectionSize/2
    
    # fill context vars (als locatie onder de 100 zit dan alleen eerste 100 opvragen anders alles)
    imageData = RemoteControl().getImageFileInfo(None, None, 100 if endLoc < 100 else None)
    retImages = imageData[startLoc-1:endLoc]

    if request.method == 'GET':
        form = ImageGaleryForm(initial={'min': startLoc ,'max': endLoc})        

    context = {
        'images': retImages,
        'imageLocation': 'http://doptrack.tudelft.nl/archive_all/',
        'thumbLocation': 'http://doptrack.tudelft.nl/Data_Download_Website/thumb/', 
        'images_form': form,
        'pid': pid,             # niet gebruikt in template, zoder deze waarde kan treesite de url niet resolven en krijg je een error op Page Title  
    }

    return render(request, 'images.html', context)


# gebruikt om benodigde data van www.n2yo.com te halen die nodig is om sateliet banen te tekenen.
#      zie   http://127.0.0.1:8000/static/satellietTrack.html
class DataForwardView(View):

    forward_host = 'http://www.n2yo.com'
    remove_from_path = '/forward'

    def get(self, request, *args, **kwargs):

        # path
        path = self.request.path
        if self.remove_from_path and path.startswith(self.remove_from_path):
            path = path[len(self.remove_from_path):]

        # url
        url = self.forward_host + path
        args = self.request.META.get('QUERY_STRING', '')
        if args:
            url = "%s?%s" % (url, args)

        # headers
        headers = {}
        if DEBUG:  print "Forward to: ", url
        responseOrg = requests.get(url, headers=headers)

        response = http.HttpResponse(content=responseOrg.content)
        response['Content-Type'] = responseOrg.headers['Content-Type']
        return response

