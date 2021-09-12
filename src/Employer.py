#!/usr/bin/env python
from marshmallow import Schema, fields, pre_load
from collections import defaultdict 
import base64
import json

class AuthorSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)

class EmployerSchema(Schema):
    employerName = fields.Str(required=True)
    employerId = fields.Integer(default=0)

class MultiLingualText(Schema):
    lang = fields.Str(required=True)
    text = fields.Str(required=True)

class Position(Schema):
    position = fields.Str(required=True)
    description = fields.Str(required=True)
    keyAchievements = fields.List(fields.Nested(MultiLingualText))
    keySkillsGathered = fields.List(fields.Nested(MultiLingualText))
    startDate = fields.Date(required=True)
    endDate = fields.Date()

class EmploymentSchema(Schema):
    employerId = fields.Integer(default=0)
    startDate = fields.Date(required=True)
    endDate = fields.Date()
    positions = fields.List(fields.Nested(Position))
    about = fields.Str(required=True)

class EmploymentHistorySchema(Schema):
    employeeId = fields.Integer(required=True)
    employmentHistory = fields.List(fields.Nested(EmploymentSchema))

class EmployeePersonalData(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    address = fields.Str(required=True)
    zipCode = fields.Str(required=True)
    city = fields.Str(required=True)
    mobilePhone = fields.Str(required=True)
    emailAddress = fields.Str(required=True)
    picture = fields.Str()

class EmployeeLanguageKnowledge(Schema):
    language = fields.Str(required=True)
    level = fields.Str(required=True)

class EmployeeSoftwareKnowledge(Schema):
    software = fields.Str(required=True)

class EmployeeKnowledge(Schema):
    languages = fields.List(fields.Nested(EmployeeLanguageKnowledge))
    softwareSkills = fields.List(fields.Str())
    programmingSkills = fields.List(fields.Str())

class EmployeeInterests(Schema):
    personal = fields.List(fields.Str())
    professional = fields.List(fields.Str())

class EmployeeSchool(Schema):
    startDate = fields.Date(required=True)
    endDate = fields.Date(required=True)
    school = fields.Str(required=True)
    education = fields.Str(required=True)
    description = fields.Str()

class EmployeeSchema(Schema):
    employeeName = fields.Str(required=True)
    employeeId = fields.Integer(default=0)
    personalData = fields.Nested(EmployeePersonalData)
    knowledge = fields.Nested(EmployeeKnowledge)
    education = fields.List(fields.Nested(EmployeeSchool))
    interests = fields.Nested(EmployeeInterests)

    @pre_load
    def decodePersonalData(self, in_data, **kwargs):
        b = base64.b64decode(in_data["encodedPersonalData"])
        s = b.decode('utf-8')
        in_data.pop("encodedPersonalData")
        in_data["personalData"] = json.loads(s)
        return in_data

class ApplicationSchema(Schema):
    applicationId = fields.Integer(default = 0)
    employeeId = fields.Integer(default = 0)
    employerId = fields.Integer(default = 0)
    position = fields.Str(required = True)
    aboutMe = fields.List(fields.Nested(MultiLingualText))
