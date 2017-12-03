#!/usr/bin/env python

import sys
import time
import os
import re
from urlparse import urlparse
from progressBar import update_prog
from commands import getoutput
from multiprocessing import Process

#squeal.py is part of the Lariat toolset

#AUTHOR: sean.m.donnelly@navy.mil

'''DESCRIPTION
  ,--.-'-,--.   #takes a URL or file with a list and attempts to determine if a site has changed since last check.
  \  /-~-\  /   #if a changelog and index exists for the site, the computed hashes will be compared with the last hashes stored.
 / )' a a `( \  #if no histroy exists then the script writes the first group of hashes to the index file and commits intitial log in the change log
( (  ,---.  ) ) #if there is no site archive and no -b option has been passed via Lariat then the directory hash is printed to the screen and the user is warned
 \ `(_o_o_)' /
  \   `-'   /
   | |---| |
   [_]   [_]
'''
banner = (
'''\033[95m
.d88888b                                      dP
88.    "'                                     88
`Y88888b. .d8888b. dP    dP .d8888b. .d8888b. 88
      `8b 88'  `88 88    88 88ooood8 88'  `88 88
d8'   .8P 88.  .88 88.  .88 88.  ... 88.  .88 88
 Y88888P  `8888P88 `88888P' `88888P' `88888P8 dP A SITE-CHANGE ALERTER
                88
                dP
\033[0m'''
)
class WGET_RECURSE(object):

        def __init__(self):
                self.wget_looper.__init__(self)

        def wgetter(self, site_url):
		site_url2 = site_url.splitlines()
                siteGrab = getoutput("wget -m -k -l 5 -t 6 -w 1 {} --no-check-certificate".format(site_url2[0]))
		site_url = urlparse(site_url)
                site_url = site_url.netloc.splitlines()
		siteHashes = getoutput("find " + site_url[0] + " -type f -exec md5sum '{}' \; | sort -k 2")
                siteHash = getoutput("find " + site_url[0]+ " -type f -exec md5sum '{}' \; | sort -k 2 | md5sum | cut -d ' ' -f 1")

		#save file hashes to temp file for possible later use
		with open('temp.txt', 'w') as d:
			d.write(siteHashes + '\n')

          #######this path is hardcoded. Please modify to meet your needs########
		changelogPath = '/home/nbt/Desktop/lariat/changelogs/'
		indexPath = '/home/nbt/Desktop/lariat/indexes/'
		changelogFile = changelogPath+site_url[0]+'-changelog.txt'
		indexFile = indexPath+site_url[0]+'-index.txt'
		timestamp = time.strftime("%c")

		if os.path.isfile(indexFile) is True and os.path.isfile(changelogFile) is True:
			dirHashTemp = ' '
			input_counter = 0
			old_group = {}
			new_group = {}
			change_group = {}
			#open the index and changelog files for reading and appending
			with open(indexFile, 'a+') as e, open(changelogFile, 'a+') as f:
				#check if the file is empty or if a previous directory hash exists
				if os.stat(indexFile).st_size == 0:
					e.write(timestamp + '\n' + siteHash + ' = directory hash\n' + siteHashes + '\n')
					f.write(timestamp + ' initial hashes generated\n')
					print("\033[92mThis is the first recorded check for {}. An initial hash group has been committed to the index file and a log entry has been added to the change log.\n\033[0m".format(site_url[0]))
				elif os.stat(indexFile).st_size > 0:
				#get the last directory hash printed to the index file
					for line in e:
						if 'directory' in line:
							indexEntry = line.split(" ")
							dirHashTemp = indexEntry[0]
							dirHashTemp = dirHashTemp.splitlines()
							dirHashTemp = dirHashTemp[0]
							input_counter += 1
					lastHash = dirHashTemp
					#if input_counter is 2 then we need to rewrite the file with only the last hash group
					if input_counter == 2:
						e.seek(0) # sets the pointer back to the first in of the file
						inverse_IC = input_counter #new counter to determine when were at the second hash group in the index file
						for line in e:
							if re.search('\d{2}:\d{2}:\d{2}',line):
								inverse_IC -= 1
							if inverse_IC == 0:
								self.old_dict_creator(line, old_group)
						#put the new sitHashes into a dict.
						self.new_dict_creator(new_group)
						#explicitly close file
						e.close()
						#rewrite the index file with only the data from the two dicts by  reopening with 'w+' option
 						with open(indexFile, 'w+') as e:
							for key in old_group:
								if re.search('\d{2}:\d{2}:\d{2}',key):
									e.write(key + '\n')
							for key in old_group:
								if '= directory hash' in key:
									e.write(old_group[key] + " "  + key)
							for key in old_group:
								if re.search('\d{2}:\d{2}:\d{2}',key):
									pass
								elif '= directory hash' in key:
									pass
								else:
									e.write(old_group[key] + " " + key)
							#start of new_group write to index file
							e.write(timestamp + '\n')
							e.write(siteHash + ' = directory hash\n')
							for key in new_group:
								e.write(new_group[key] + " " + key)
						if siteHash == lastHash:
							#write to change log file with time stamp and 'SAME'
							f.write(timestamp + " no change\n")
						elif siteHash != lastHash:
							#use a dictionary comprehension to get different keys and different values for same keys
							self.dict_diff(old_group, new_group, change_group, f, site_url)
					elif input_counter == 1:
						if siteHash != lastHash:
							self.dict_diff(old_group, new_group, change_group, f, site_url)
						elif siteHash == lastHash:
							e.write(timestamp + '\n' + siteHash + ' = directory hash\n' + siteHashes + '\n')
							f.write(timestamp + " no change\n")
							print("{} change log and index files have been updated".format(site_url[0]))
				else:
					print("\033[91m**{} failed because there was an issue with the index or changelog files**\033[0m".format(site_url[0]))
		else:
			print("\033[93m*WARNING*\033[0m the site '{}' does not have the necessary file archive. Please run Lariate with the BuilDir option\n\n".format(site_url[0]))
			sys.exit(0)
		#purge the wget dir
                removal = getoutput("rm -rf {} 2 > /dev/null".format(site_url[0]))
                #remove the temp file holding site hashes and file names
                removal = getoutput("rm temp.txt 2 > /dev/null")

        def old_dict_creator(self, line, old_group):
		#put the rest of the data into old_group dict
                #handle timestamp and last hash lines
                if re.search('\d{2}:\d{2}:\d{2}',line):
			line = line.rsplit(' ', 1)
                        stamp = line[0]
                        #empty value in dictionary for timestamp of old hash group
                        old_group[stamp] = ''

                elif '= directory hash' in line:
                        line = line.split(' ', 1)
                        hash = line[0]
                        text = line[1]
                        old_group[text] = hash

                else:
                        line = line.split(' ', 1)
			hash = line[0]
			fileName = line[1]
                        old_group[fileName] = hash
		return old_group

	def new_dict_creator(self, new_group):
		#puts the new sitHashes into a dict.
                with open('temp.txt', 'r') as g:
                	for line in g:
                		line = line.split(' ', 1)
				hash = line[0]
				fileName = line[1]
                        	new_group[fileName] = hash
		return new_group

	def dict_diff(self, old_group, new_group, change_group, f, site_url):
	#uses a dictionary comprehension to get different keys and different values for same keys
		timestamp = time.strftime("%c")
        	try:
			for key in old_group:
        			if key in new_group:
                        		if old_group[key] not in new_group[key]:
                                		change_group[key] = new_group[key]
                        	#if a key from old_group doesn't exist in new_group then add to change_group dict with value 'removed'
                        	elif key not in new_group:
					if re.search('\d{2}:\d{2}:\d{2}',key):
                                 		pass
                                	elif '= directory hash' in key:
                                       		pass
                        	 	else:
						change_group[key] = 'removed'
                	#if a key from new_group doesn't exist in old_group then add it to change_group dict with value 'added'
                	for key in new_group:
                		if key not in old_group:
					if re.search('\d{2}:\d{2}:\d{2}',key):
                                        	pass
                                	elif '= directory hash' in key:
                                        	pass
					else:
                        			change_group[key] = '  added'
                 	#write to changelog file with timestamp 'DIFFERENT', new line and indentation and change_group values
			f.write(timestamp + " DIFFERENT\n\t\t\t")
                	print('\033[93m the following modifications have been made to {} - findings have been recorded in the site changelog.\n\033[0m'.format(site_url[0]))
                	#tabCheck = 0
                	for key in change_group:
                		if re.search('\d{2}:\d{2}:\d{2}',key):
                        		pass
                      		elif '= directory hash' in key:
                        		pass
                        	elif 'removed' not in change_group[key] and '  added' not in change_group[key]:
                        		f.write('changed ' + key + '\t\t\t')
                                	print('\033[93m\t(+)\033[0m changed {}'.format(key))
                         #       	tabCheck += 1
                        	#if tabCheck > 1:
                        #f.write('\t\t\t')
                        for key in change_group:
                        	if 'removed' in change_group[key] or '  added' in change_group[key]:
                                	f.write(change_group[key] + " " + key + '\t\t\t')
                                        print ('\033[93m\t(+)\033[0m {} {}'.format(change_group[key], key))
                        f.write('\n')

			return old_group, new_group, change_group
		except KeyboardInterrupt:
			#purge the wget dir
	                removal = getoutput("rm -rf {} 2 > /dev/null".format(site_url[0]))
                	#remove the temp file holding site hashes and file names
                	removal = getoutput("rm temp.txt 2 > /dev/null")


	def wget_looper(self,input,runs):

		run_num = 0
                for site_url in input:
			#run_num +=1
			#update_prog(runs,run_num + 1)
			getem = Process(target=self.wgetter, args=(site_url,))
                        getem.start()

if __name__ == '__main__':

	if len(sys.argv) != 2:
	      print 'Usage: {} <url list file>'.format(sys.argv[0])
              sys.exit(0)

	runs = getoutput("wc -l < {} 2> /dev/null".format(sys.argv[1]))
	inFile = sys.argv[1]
        input  = open(inFile, "r")
	print(banner)
	#print("\033[96m**Squeal site hashing takes an average of two minutes. Hang tight!**\n \033[0m")
	print("\033[96m**generating hashes for each URL in {}. This can take awhile.**\033[0m \n".format(inFile))
	try:
	       WGET_RECURSE().wget_looper(input,runs)
	       sys.stdout.write("\n")
        except KeyboardInterrupt:
	       pass

#ADDITIONAL INFO

'''clarification regarding wget switches:

-m recursively grab pages & images
-k modifies links in the html to point to local files
-E saves HTML & CSS with proper extensions
-l depth of spidering
-t number of retries after failed attempts
-w tells wget to wait x seconds before grabbing the next file (keeps from crashing a server)
'''
