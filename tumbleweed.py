#!/usr/bin/env python

import sys
import time
from progressBar import update_prog
from commands import getoutput
from multiprocessing import Process

#tumbleweed.py is part of the Lariat tool

#Author: sean.m.donnelly@navy.mil

'''takes a file name as a parameter and determines if the URLs in the file are operational and if
they redirect (useful knowledge to troubleshoot HP Web Inspect failed scans).  Script completion results in two text files; first file
"sitesToScan.txt" contains a list of "up" sites and states whether or not they are redirected.
Second file is titled  "downSites.txt" which contains URLs that can be omitted from scheduled scans.


#TO DO List
# determine site up/down time, determine and write the following info to the summary file:
smart card enabled: (yes/no)
redirected:(yes/no)
ip address:
site PoC:
creation date:
domain:
up/down time:
server details:
'''
banner = (
'''\033[92m
		     .    _    +     .  ______   .          .     '      .            '+
  (      /|\      _   _|      \___   .   +    '    .         *
    /\  ||||| .  | | |   | |      |       .    '                    .    '
 __||||_|||||____| |_|_____________\________________________________________
 . |||| |||||  /\   _____      _____  .   .       .             .       .
  . \|`-'|||| ||||    __________            .
     \__ |||| ||||      .          .     .     .        -            .   .
  __    ||||`-'|||  .       .    __________
 .    . |||| ___/  ___________             .
 _   ___|||||__  _           .          _
      _ `---'    .   .    .   _   .   .    .
 _  ^      .  -    .    -    .       -    .    .  .      -   .     .    -
\033[0m'''
)

class CURL_SWEEP(object):

        def __init__(self):
                self.curl_sweeper.__init__(self)

        def curler(self, site_url, scanList, downList):
                """thread curler function"""
                line = getoutput("curl -k -I -L  {} 2> /dev/null".format(site_url))
 		while True:
                        if line.find("200")  > -1:
			        if line.find("301") > -1:
                                        #write to upSites.txt with a redirect tag
                                        scanList.writelines("{} \033[093m REDIRECT \033[0m".format(site_url))
                                        break
				else:
					#write to upSites.txt file
					scanList.writelines("{}".format(site_url))
                                	break

			elif line.find("timed out") or line.find("Could not resolve host:"):
				#print down site url to downSites.txt
				downList.writelines("{}".format(site_url))
                                break
			elif line.find("404"):
				scanList.writelines("{} \033[092m FORBIDDEN \033[0m".format(site_url))
                        else:
                                exit(0)

		scanList.close()
		downList.close()

        def curl_sweeper(self,input,runs,scanList,downList):
		run_num = 0
                for site_url in input:
                        curl = Process(target=self.curler, args=(site_url,scanList,downList,))
                        curl.start()
			run_num += 1
                        update_prog(runs,run_num + 1)

if __name__ == '__main__':

	if len(sys.argv) != 2:
	      print 'Usage: {} <url list file>'.format(sys.argv[0])
              sys.exit(0)

	runs = getoutput("wc -l < {} 2> /dev/null".format(sys.argv[1]))
	inFile = sys.argv[1]
        input  = open(inFile, "r")
	try:
               print "\033[92m Tumbleweed Pre-scan \033[0m"
	       print "\033[93m Checking " + runs + " URLs \033[0m"
	       print banner
	       time.sleep(1)
	       getoutput("rm downSites.txt upSites.txt 2> /dev/null")
               scanList = open("upSites.txt", "a")
               downList = open("downSites.txt", "a")
	       CURL_SWEEP().curl_sweeper(input,runs,scanList,downList)
	       sys.stdout.write("\n")
        except KeyboardInterrupt:
               pass




