'''
Created on 8 feb. 2016

@author: richardberg
'''

from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=30)
    start = models.DateField(blank=False, null=False)
    end = models.DateField(blank=False, null=False)
    timeslotDuration = models.TimeField(blank=False, null=False)
    docent = models.ForeignKey(User)

    # students = models.ManyToManyField('Student', through='CourseStudent')
    # students = models.ManyToManyField('User', through='CourseStudent')

    def __str__(self):
        return self.name + ' | ' + str(self.start) + "  " + str(self.end) + "  " + str(self.timeslotDuration)

    def save(self):
        super(Course, self).save()

    class Meta:
        managed = True
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


# TODO (Beter default django User gebruiken.)
'''class Student(models.Model):
    name = models.CharField('name', unique=False, max_length=20, blank=False)
    password = models.CharField('password', unique=False, max_length=20, blank=False)
    last_login = models.DateTimeField(blank=True, null=True)     # Veld toegevoegd voor gebruik in django.authorization

    courses = models.ManyToManyField('Course', through='CourseStudent')
    is_staff = False

    def __str__(self):
        return str(self.id) + "  " + self.name

    class Meta:
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    # toegevoegd vanwege gebruik in django.authorization
    #    The default Anonomous objeject has same method and always returns  false
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    #def is_staff(self):
    #    return False

    def has_module_perms(self, module):
        return False
'''


class CourseStudent(models.Model):
    # student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)

    # user = models.OneToOneField(User, on_delete=models.CASCADE)    # user kolom word unique gemaakt, ongewenst als je gebruiker in meerdere courses wil gebruiken.
    user = models.ForeignKey(User)

    def __str__(self):
        return 'CourseStudent'

    class Meta:
        managed = True

    def save(self):
        super(CourseStudent, self).save()


class TimeSlot(models.Model):
    start = models.DateTimeField(blank=False, null=False)
    modified = models.DateField(blank=False, null=False)
    coursestudent = models.ForeignKey('CourseStudent')

    def __str__(self):
        return 'TimeSlot: ' + str(self.id) + "  " + str(self.start) + "  " + str(self.modified)

    class Meta:
        managed = True

    def save(self):
        super(TimeSlot, self).save()
