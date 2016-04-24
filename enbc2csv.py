#!/usr/bin/env/python
#
# Copyright 2016
# John P. Davis
# jd@pauldavisautomation.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
import argparse
import sys
import csv
import re

global CSV_FILEPATH

# define the headers for the CSV file
global CSV_HEADERS
CSV_HEADERS = ['First Name', 'Last Name', 'Company Name and Branch', 'Job Title of Contact', 'Phone', 'E-mail Address', 'Mailing Address Line 1']

def parseArgs():

	parser = argparse.ArgumentParser(description="This program takes html files of business cards/contacts exported from Evernote and converts them into a CSV file that may be imported into something else.\n\nUsage is as follows: enbc2csv.py *.html -o my_contacts.csv")
	
	#now specify the options the program takes from the user
	parser.add_argument("-o", "--outfile", help="Full path the CSV file that will contain the formatted output from the input files")
	
	#allow multiple input files of type HTML (eventually, this will have to be valid Evernote HTML
	parser.add_argument("-i", "--input_file", nargs="+", help="A single - or many - Evernote HTML contact files")
	
	#add verbosity control
	parser.add_argument("-v", "--verbose", help="Controls output verbosity", action="store_true")

	#check length of args - if it is 0, display help
	if len(sys.argv) == 1:
		parser.print_help()
		exit(0)
	
	args = parser.parse_args()

	# if there is no outfile, bail
	if args.outfile == None:
		print("You must specify an output file")
		exit(1)

	global CSV_FILEPATH 
	CSV_FILEPATH = args.outfile

	if args.verbose:
		processHTMLFiles(args.input_file, 1)

	else:
		processHTMLFiles(args.input_file, 0)

def setupCSVFile():

	try:	
		outfile = open(CSV_FILEPATH, 'w')
	except(OSError, IOError) as e:
		print("Could not open outfile %s with error %s" % CSV_FILEPATH, e)
		exit(1)
	
	writer = csv.DictWriter(outfile, fieldnames=CSV_HEADERS)
	writer.writeheader()
	outfile.close()
	print("Empty CSV File Successfully Created with headers: ")

	for header in CSV_HEADERS:
		print(header)

	#empty line for formatting
	print

def processHTMLFiles(fileNames, verbose):
	
	#setup CSV file
	setupCSVFile()

	#output file variable
	outfile = None

	#variable to hold valid files
	valid_files = list()
	found_attrs = list()
	
	#bad file counter for non-verbose output showing how many non-EN files were read
	badFileCounter = 0
	
	#open up output CSV file
	try: 
		outfile = open(CSV_FILEPATH, 'a')
	except(OSError, IOError) as e:
		print("Could not open outfile %s with error %s" % CSV_FILEPATH, e)
		exit(1)

	#check validity of files and process them
	for x in fileNames:
		
		try:
			f=open(x, 'r')

		except(OSError, IOError) as e:
			if verbose == 1:
				print("Could not open file %s with error %s" % x, e)
				break

			else:
				break

		html_string = BeautifulSoup(f.read(), 'html.parser')

		# first, check to make sure the files are valid Evernote HTML
		valid = None
		for meta_tag in html_string.find_all('meta'):
			if meta_tag.get('name') == 'content-class' and meta_tag.get('content').find('evernote.contact.1') != -1:
				valid = True
				valid_files.append(x)
				break

		if not valid:
			badFileCounter = badFileCounter+1

			if verbose == 1:
				print("!!! File %s is not a valid EN HTML file, skipping..." % f.name)
				print

		f.close()
		
	for en_file in valid_files:
		
		first = ""
		last = ""
		company = ""
		title = ""
		phone = ""
		email = ""
		mailing_address = ""
		mailing_city = ""
		state = ""
		postal = ""
		country = ""
		
		fieldType = None

		try:
			f=open(en_file, 'r')

		except(OSError, IOError) as e:
			print("Could not open file %s with error %s" % x, e)
			break
	
		# have to seek to beginning of file since we read it in the previous operation
		html_string = BeautifulSoup(f.read(), 'html.parser')

		# file is valid, so start processing it
		print("**********Processing file: %s" % f.name)
		
		for x_field in html_string.find_all(style=re.compile('^x-evernote:display-as')):
			name = x_field.contents[0]
		
			if name != 'x-evernote:display-as':
				# split to get first name and last name
				# TODO - have this handle titles, like PhD
				names = unicode.split(unicode(name.string))
				if len(names) == 3:
					first = names[0]
					last = names[2]

				elif len(names) == 2:
					first = names[0]
					last = names[1]

				else:
					first = names[0]
					last = ""
			
		# title
		for x_field in html_string.find_all(style=re.compile('^x-evernote:contact-title')):
			if len(x_field.contents)  and x_field.contents[0] != 'x-evernote:contact-title' > 0:
				title = x_field.contents[0]

		# organization
		for x_field in html_string.find_all(style=re.compile('^x-evernote:contact-org')):
			if len(x_field.contents) > 0 and x_field.contents[0] != 'x-evernote:contact-org':
				company = x_field.contents[0]
		
		# mobile, phone, fax, address
		# email = 0
		# mobile = 1
		# phone = 2
		# fax = 3
		# address = 4
		for x_field in html_string.findAll(style='float: left; clear: left; min-width: 400px;overflow:hidden; _overflow:visible; zoom:1;'):
			for name_field in x_field.findAll(style=re.compile('^x-evernote:context;')):
				if re.search('email', name_field.contents[0], re.IGNORECASE):
					fieldType = 0
					
				if re.search('mobile', name_field.contents[0], re.IGNORECASE):
					fieldType = 1 
				
				if re.search('phone', name_field.contents[0], re.IGNORECASE):
					fieldType = 2

				if re.search('fax', name_field.contents[0], re.IGNORECASE):
					fieldType = 3

				if re.search('address', name_field.contents[0], re.IGNORECASE):
					fieldType = 4

			for value_field in x_field.findAll(style=re.compile('^x-evernote:value')):
				if len(value_field.contents) > 0 and len(value_field.contents[0]) > 0:
					
					# if the value is a link, it is likely an address
					if value_field.a and fieldType == 4:
						if value_field.a.string.find('linkedin') == -1:
							mailing_address = value_field.a.string.replace("\n", " ")
					
					if fieldType == 0 and value_field.a != None:
						email = value_field.a.string

					# mobile number first, but if there is a phone number, that overwrites the value
					if fieldType == 1 and value_field.a == None:
						 phone = value_field.contents[0]	
					
					elif fieldType == 2 and value_field.a == None:
						phone = value_field.contents[0]

		print("Saving %s %s %s %s %s %s %s to file" % (first, last, company, title, phone, email, mailing_address))
		print
		#output = CSVObject(first, last, company, title, phone, email, mailing_address) 
		#output.write(outfile)	
		writer = csv.writer(outfile, dialect='excel')
		writer.writerow([first.encode('utf-8'), last.encode('utf-8'), company.encode('utf-8'), title.encode('utf-8'), phone.encode('utf-8'), email.encode('utf-8'), mailing_address.encode('utf-8')])
		f.close()
	
	#clean up
	outfile.close()
	print
	print("!!! %d files were not in Evernote format and were NOT parsed" % badFileCounter)


# the Python interpreter looks for this bit of code. This is where the actual program starts executing
if __name__ == '__main__':
	
	parseArgs()
	exit(0)






