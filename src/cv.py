#!/usr/bin/env python
import os
import locale
import json
from pprint import pprint
import argparse

from Employer import ApplicationSchema, EmployerSchema, EmployeeSchema, EmploymentHistorySchema, AuthorSchema

from LatexHelper import LatexHelper
basedir = '.'

class Main():
	def __init__(self):
		self.employers = []
		self.employmenthistory = []
		self.employees = []
		self.applications = []
		self.employerid = 0
		self.employeeid = 0

		parser = argparse.ArgumentParser()
		parser.add_argument("--lang", type=str, help="The output language", choices=[ "en" ], default="en")
		parser.add_argument("-d", "--debug", help="Turn on debugging", action="store_true")
		parser.add_argument("-t", "--template", help="LaTeX Jinja2-template to use for formatting", choices=[ "default" ], default="default")
		parser.add_argument("-c", "--colorset", help="Colorset to use", choices=[ "navyblue", "grey", "gold" ], default="grey" )
		parser.add_argument("-s", "--skipcover", help="Skip the cover letter", action="store_true" )
		parser.add_argument("application", type=int, help="The application id from application database")
		args = parser.parse_args()

#		if args.lang == "sv":
#  			print("Swedish selected as language.")
#		else:
#  			print("English selected as default language")

		colorconfig =  {
			"colordefinitions": [
				{ "name": "airforceblue", "rgb":  [ 0.36, 0.54, 0.66 ]}
				,{ "name": "navyblue", "rgb":     [ 0.00, 0.00, 0.50 ]}
				,{ "name": "armygreen", "rgb":    [ 0.29, 0.33, 0.13 ]}
				,{ "name": "arsenic", "rgb":      [ 0.23, 0.27, 0.29 ]}
				,{ "name": "ceruleanblue", "rgb": [ 0.16, 0.32, 0.75 ]}
				,{ "name": "paynesgrey", "rgb":   [ 0.25, 0.00, 0.50 ]}
				,{ "name": "phtalogreen", "rgb":  [ 0.07, 0.21, 0.14 ]}
				,{ "name": "taupe", "rgb":        [ 0.28, 0.24, 0.20 ]}
				,{ "name": "gamboge", "rgb":      [ 0.89, 0.61, 0.06 ]}
				,{ "name": "ginger", "rgb":       [ 0.69, 0.40, 0.00 ]}
				,{ "name": "uscgold", "rgb":      [ 1.00, 0.80, 0.00 ]}

			],"colormapping": {
				"navyblue": {
					"color": "airforceblue"
					,"separator": "armygreen"
					,"header": "airforceblue"
					,"contact": "arsenic"
				},"grey": {
					"color": "paynesgrey"
					,"separator": "phtalogreen"
					,"header": "taupe"
					,"contact": "phtalogreen"
				}, "gold": {
					"color": "uscgold"
					,"separator": "ginger"
					,"header": "gamboge"
					,"contact": "uscgold"
				}
			}
		}

		applicationid = args.application
		self.template = args.template

		try:
			self.applications = self.loadDatabase(os.path.join(basedir, 'data', 'applications.json'), "ApplicationSchema")  
			self.employers = self.loadDatabase(os.path.join(basedir, 'data', 'employers.json'), "EmployerSchema")
			self.employees = self.loadDatabase(os.path.join(basedir, 'data', 'employees.json'), "EmployeeSchema")
			self.employmenthistory = self.loadDatabase(os.path.join(basedir, 'data', 'employmenthistory.json'), "EmploymentHistorySchema")
			self.author = self.loadDatabase(os.path.join(basedir, 'data', 'author.json'), "AuthorSchema", many=False)

			self.config = { "lang": args.lang, "skipcover": args.skipcover, "colorconfig": colorconfig, "colorset": args.colorset }

		except IOError:
			print('IO Error while reading json input')
		except TypeError as te:
			print('Type Error trying to see result: {}'.format(te))

		for application in self.applications:
			if application['applicationId'] == applicationid:
				print('found application with id {}'.format(applicationid))
				self.employerid = application['employerId']
				self.employeeid = application['employeeId']

				for employee in self.employees:
					if employee['employeeId'] == self.employeeid:
						print('Found employee with id {}'.format(self.employeeid))

					for employer in self.employers:
						if employer['employerId'] == self.employerid:
							print('Found employer with id {}'.format(self.employerid))
							print('Creating a job application for employee {} for position with employer {}\n\tUsing template "{}", colorset "{}"'.format(employee['employeeId'], employer['employerId'], args.template, args.colorset))

							h = LatexHelper()
							h.setTemplate(self.template)
							h.createLatexFile(application=application, employees=self.employees
							                  ,employers=self.employers, employmenthistory=self.employmenthistory
											  ,config=self.config, author=self.author)
							exit(0)

					print('I am bailing out. No such employer id: {}, referenced from applicationId: {}'.format(application['employerId'],applicationid))
					exit(2)

				print('I am bailing out. No such employee id: {}, referenced from applicationId: {}'.format(application['employeeId'], applicationid))
				exit(2)

		print('I am bailing out. No such application id: {}'.format(applicationid))
		exit(2)

	def loadDatabase(self, path, schemaname, many=True):
		with open(path) as database_file:
			tempschema = globals()[schemaname](many=many)
			dbobj = tempschema.loads(database_file.read())
			return dbobj

m = Main()