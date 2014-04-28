import os
import re
import csv
import sys

OUTPUT_FILENAME = "emails_set.csv"
PATTERN_EMAIL = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')

file_extensions = sys.argv[1:] or ['.txt', '.csv']

emails = dict()
def process(dirname, filename):
	data = open(os.path.join(dirname, filename), 'rb')
	for line in data:
		for match in PATTERN_EMAIL.findall(line):
			emails[match[0]] = dirname
			
def show_progress(current, total):
	percent = int(current / float(total) * 100)
	sys.stdout.write("\r%s%s completed" % (percent, "%"))
	sys.stdout.flush()

total_folders = 0
for dirname, dirnames, filenames in os.walk('.'):
	total_folders += 1

folder_counter = 0
for dirname, dirnames, filenames in os.walk('.'):
	folder_counter += 1
	for filename in filenames:
		for file_ext in file_extensions:
			if filename.endswith(file_ext):
				process(dirname, filename)
				break

	show_progress(folder_counter, total_folders)

if not emails:
	print 'No emails found'
	exit(1)
	
print '\nFound %s emails' % (len(emails))
emails_sorted = sorted(emails.keys())

output_file = open(OUTPUT_FILENAME, 'wb')
wr = csv.writer(output_file)
for email in emails_sorted:
	wr.writerow([email])

output_file.close()