
# NIET GEBRUIKT, het lukte niet om studenten handmatig toe te voegen en die aan course te koppelen

from django.contrib import admin
from models import (Course, CourseStudent, TimeSlot)


from django import forms
'''
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ['name']


class CourseStudentsInline(admin.TabularInline):
    model = CourseStudent
    list_display = ('studentX')
    readonly_fields = ('studentX', )
    extra = 0
    verbose_name = "student"
    verbose_name_plural = "students"
    form = StudentForm

    def studentX(self, obj):
        val = 'blabla: ' + str(obj.student.id) + ' ' + obj.student.name
        return val
    studentX.short_description = 'lala'
'''

'''
class StudentCoursesInline(CourseStudentsInline):
    verbose_name = "Course"
    verbose_name_plural = "Courses"
    fields = ('id', ('Course', 'Student'),)
    readonly_fields = ('descrX', )

    def descrX(self, obj):
        return 'blabla: ' + obj.student.id + ' ' + obj.student.name
    descrX.short_description = 'lala'


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentCoursesInline,]
    list_display = ['id', 'name']  
'''
'''

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseStudentsInline,]
    list_display = ['name', 'start', 'end', 'timeslotDuration']
    search_fields = ['name', 'start']
    # form = StudentForm

    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }


#admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
'''
