#!/usr/bin/env python

import sys
import os
import time
from progressBar import update_prog
from urlparse import urlparse
from multiprocessing import Process
from commands import getoutput

#BuilDir.py is part of the Lariat Tool Suite
#check if changelogs, summaries, and indexes directories exist and creates them if not
#check if the command line option provided is a file or a single URL (-u or -s)
#calls the appropriate method to check and create files

banner = (
"""\033[93m
    @
    )
   (_m_\
   \\" _.`~.
  `(#'/.\)
     .>' (_--,
  _=/d  . ^\
 ~~ \)-'   '
    / |
\033[0m"""
)

#the following directory paths are hardcoded.  Modify them to fit your need
changelogs = '/root/lariat/changelogs/'
summaries = '/root/lariat/summaries/'
indexes = '/root/lariat/indexes/'
class BUILDIR(object):

	def __init__(self):
        	        self.dir_builder.__init__(self)

	def buildir_function(self, site_url):
		if os.path.isdir(changelogs) is False:
       			os.mkdir(changelogs)

		if os.path.isdir(summaries) is False:
        		os.mkdir(summaries)

		if os.path.isdir(indexes) is False:
			os.mkdir(indexes)
		#strip the http(s):// off the url before passing
		site_url = urlparse(site_url)
		site_url = site_url.netloc.splitlines()
		changelogFile = (changelogs + site_url[0] + '-changelog.txt')
		summaryFile = (summaries + site_url[0] + '-summary.txt')
		indexFile = (indexes + site_url[0] + '-index.txt')

		if os.path.isfile(changelogFile) is True:
			pass
		else:
			#make <url>-changelog.txt
			open(changelogFile, 'w')

		if os.path.isfile(summaryFile) is True:
			pass
		else:
			#make <url>-summary.txt
			open(summaryFile, 'w')

		if os.path.isfile(indexFile) is True:
			pass
		else:
			#make <url>-index.txt
			open(indexFile, 'w')

	def dir_builder(self, url_list, runs2):

		run_num = 0
		for site_url in url_list:
			build = Process(target=self.buildir_function, args=(site_url,))
               		build.start()
			run_num += 1
                        update_prog(runs2,run_num + 1)

if __name__ == '__main__':

	input = sys.argv[1]
	runs = getoutput("wc -l < {} 2> /dev/null".format(sys.argv[1]))
        runs2 = int(runs)
	try:
		url_list = open(input, 'r')
		BUILDIR().dir_builder(url_list,runs2)
		sys.stdout.write('\n')
	except:
		sys.stdout.write('processed a single URL\n')
		BUILDIR().buildir_function(input)
