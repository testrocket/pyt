import os
import re
import csv
import sys

OUTPUT_FILENAME = "emails_set.csv"
PATTERN_EMAIL = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')

def process(emails, dirname, filename):
	data = open(os.path.join(dirname, filename), 'rb')
	for line in data:
		for match in PATTERN_EMAIL.findall(line):
			emails[match[0]] = dirname
			
def show_progress(current, total):
	percent = int(current / float(total) * 100)
	sys.stdout.write("\rSearching for emails in files - %s%s completed..." % (percent, "%"))
	sys.stdout.flush()
	
def calc_folders_count():
	total_folders = 0
	for dirname, dirnames, filenames in os.walk('.'):
		total_folders += 1
	return total_folders
	
def emails_search(file_extensions):	
	folder_counter = 0
	total_folders = calc_folders_count()

	emails = dict()
	for dirname, dirnames, filenames in os.walk('.'):
		folder_counter += 1
		for filename in filenames:
			for file_ext in file_extensions:
				if filename.endswith(file_ext):
					process(emails, dirname, filename)
					break

		show_progress(folder_counter, total_folders)
	return emails

file_extensions = sys.argv[1:] or ['.txt', '.csv']
emails = emails_search(file_extensions)
if not emails:
	print 'No emails found.'
	exit(1)
	
print '\nFound %s emails in directories:' % len(emails)

directories = set(emails.values())
for directory in directories:
	print directory

emails_sorted = sorted(emails.keys())

output_file = open(OUTPUT_FILENAME, 'wb')
wr = csv.writer(output_file)
for email in emails_sorted:
	wr.writerow([email])

output_file.close()
