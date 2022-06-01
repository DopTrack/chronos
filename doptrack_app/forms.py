'''
Created on 9 feb. 2016

@author: richardberg
'''
from django import forms
from django.forms.formsets import BaseFormSet
from captcha.fields import CaptchaField

UI_DATE_FORMAT = '%d/%m/%Y'


class RequestForm(forms.Form):
    body = forms.CharField(label='Message', widget=forms.Textarea(attrs={'rows':17,'cols':70}))
    replyEmail = forms.CharField(label='Reply email', max_length=100 )
    captcha = CaptchaField()


class LoginForm(forms.Form):
    user = forms.CharField(label='User name', max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    next = ''


class StudentForm(forms.Form):
    name = forms.CharField(label='User name', max_length=32, required=False)
    password = forms.CharField(label='Password', max_length=32, required=False)


class FilesForm(forms.Form):
    days = forms.CharField(label='Limit days', max_length=4)

class ImageGaleryForm(forms.Form):
    min = forms.IntegerField(label='from image', min_value=1, max_value=99999)
    max = forms.IntegerField(label='up to image', min_value=1, max_value=99999)



class CourseForm(forms.Form):

    name = forms.CharField(label=u'Course name',
                           max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': 'Course name', }))
    start = forms.DateField(label=u'Course start',
                            input_formats=[UI_DATE_FORMAT],
                            required=True,
                            widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', }, format=[UI_DATE_FORMAT]))
    end = forms.DateField(label=u'Course end',
                          input_formats=[UI_DATE_FORMAT],
                          required=True,
                          widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', }, format=[UI_DATE_FORMAT]))
    timeslotDuration = forms.TimeField(label='Time slot size',
                                       required=True,
                                       widget=forms.TimeInput(attrs={'placeholder': 'hh:mm:ss', }))
    file = forms.FileField(label='Upload student names',
                           required=False)

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)
        super(CourseForm, self).__init__(*args, **kwargs)

        if self.course:
            self.fields['name'].initial = self.course.name if self.course.name else ''
            self.fields['start'].initial = self.course.start.strftime(UI_DATE_FORMAT) if self.course.start else ''
            self.fields['end'].initial = self.course.end.strftime(UI_DATE_FORMAT) if self.course.end else ''
            self.fields['timeslotDuration'].initial = self.course.timeslotDuration \
                if self.course.timeslotDuration else '00:30:00'


class BaseStudentFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        students = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']

                # Check that no two links have the same anchor or URL
                if name:
                    if name in students:
                        duplicates = True
                    students.append(name)

                if duplicates:
                    raise forms.ValidationError(
                        'duplicate student found',
                        code='duplicate_links'
                    )


class ServerControlForm(forms.Form):
    satellitename = forms.CharField(label='Satellitename', max_length=20)
    noradid = forms.CharField(label='Noradid', max_length=10)
    starttime = forms.CharField(label='Starttime', max_length=100)
    length = forms.CharField(label='Length', max_length=6)
    frequency = forms.CharField(label='Frequency', max_length=15)

# The rest are tests, and are not used yet
#class NameForm(forms.Form):
    #your_name = forms.CharField(label='title', max_length=100)
#    pass

