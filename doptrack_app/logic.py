import datetime
import csv

from .models import TimeSlot
from .remote import RemoteControl

'''
Created on 11 aug. 2016

@author: richardberg
'''


# haal timeslots op en verbind aangrenzende aan elkaar
def getTimslots(userId, bottomDateLimit=None):
    if bottomDateLimit:
        timeslotList = TimeSlot.objects.filter(start__gt=bottomDateLimit, coursestudent__user__id=userId) \
            .select_related('coursestudent', 'coursestudent__course').order_by('start').all()
    else:
        timeslotList = TimeSlot.objects.filter(coursestudent__user__id=userId) \
            .select_related('coursestudent', 'coursestudent__course').order_by('start').all()

    retList = []

    slotStart = None
    slotEnd = None
    for ts in timeslotList:

        if (not(slotStart) or slotEnd < ts.start):
            if slotStart:
                retList.append({'start': slotStart, 'end': slotEnd})
            slotStart = ts.start
        slotEnd = ts.start + datetime.timedelta(hours=ts.coursestudent.course.timeslotDuration.hour,
                                                minutes=ts.coursestudent.course.timeslotDuration.minute,
                                                seconds=ts.coursestudent.course.timeslotDuration.second)

    if (slotStart and slotEnd):
        retList.append({'start': slotStart, 'end': slotEnd})
    return retList


# bepaal of de gegeven tijd ergens in een tijdslot valt van deze gebruiker
def isRecordingInTimeslot(userId, startRecording, lengthRecordingSec):
    bottomDateLimit = datetime.datetime.now() - datetime.timedelta(hours=24)     # AANNAME: course.timeslotDuration is not larger than 24h
    for slot in getTimslots(userId, bottomDateLimit):
        if (slot['start'] <= startRecording and startRecording + datetime.timedelta(seconds=lengthRecordingSec) <= slot['end']):
            return True
    return False


def getEndCurrentRecording(safeMarginSec=5, schedules=None):
    if not schedules:
        schedules = RemoteControl().getScheduleFileInfo()
    for schedule in schedules:
        startSchedule = schedule['time'] - datetime.timedelta(seconds=safeMarginSec)
        endSchedule = startSchedule + datetime.timedelta(seconds=schedule['length'] + safeMarginSec)
        if startSchedule < datetime.datetime.now() < endSchedule:
            return endSchedule
    return None


# verwerk een bestand tot een dict[studentName] = {'password': password}
def handleStudentFile(uploadStudentsFile):
    studentDict = {}
    print uploadStudentsFile.name
    if uploadStudentsFile.name.endswith('.xlsx'):
        print "excel not supportd yet"   # zie sms.py project scriptje 10 regels python nodig
    if uploadStudentsFile.name.endswith('.txt'):

        dialect = csv.Sniffer().sniff(uploadStudentsFile.read(1024))
        uploadStudentsFile.seek(0)

        reader = csv.reader(uploadStudentsFile, dialect)

        rowCnt = 0
        for row in reader:
            rowCnt += 1

            username = str(row[0]).strip()
            password = str(row[1]).strip()

            if len(username) > 0:
                studentDict[username] = {'password': password}
    return studentDict
