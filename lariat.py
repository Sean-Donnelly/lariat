#!/usr/bin/env python

import buildir
import squeal
import tumbleweed
import argparse
import sys
import time
import progressBar
from subprocess import Popen, PIPE
from commands import getoutput
from multiprocessing import Process

banner = (
"""
   ooooo                              o88              o8
    888          ooooooo   oo oooooo  oooo   ooooooo o888oo
    888          ooooo888   888    888 888   ooooo888 888\033[91m
    888      o 888    888   888        888 888    888 888
   o888ooooo88  88ooo88 8o o888o      o888o 88ooo88 8o 888o
\033[0m"""
)
sys.stdout.write(banner + '\n')
text =(
"""\033[093m The Lariat Toolset is a compilation of tools used for gathering, updating, and organizing website information to aid in automated web vulnerability scanning.\033[0m
"""
)
parser = argparse.ArgumentParser(description=text)
parser.add_argument('-A', "--all", help='run all tools', action="store_true")
parser.add_argument('-s', "--site", help='pass a single URL')
parser.add_argument('-u', "--list",  help='pass a directory name containing a list of URLs')
parser.add_argument('-b', "--buildir", help='run BuilDir:for each URL, checks if a directory exists and if not creates it, changelog.txt, and summary.txt', action="store_true")
parser.add_argument('-T', "--tumbleweed", help='run Tumbleweed', action="store_true")
parser.add_argument('-S', "--squeal", help='run Squeal', action="store_true")
parser.add_argument('-a', "--autoscan", help='run autoscan (requires -t option)', action="store_true")

args = vars(parser.parse_args())
if args['autoscan'] is False and args['buildir'] is False and args['tumbleweed'] is False and args['squeal'] is False:
	sys.stdout.write("\033[93m PLEASE RUN LARIAT WITH AT LEAST ONE ARGUMENT\n\033[0m")

#if a url list is provided, open the file then pass it to BUILDIR to run through the URLs
runs = getoutput("wc -l < {} 2> /dev/null".format(args['list']))
runs2 = int(runs)
inUrl = args['site']
inFile = args['list']

try:
	print("\033[93mProcessing {} File Containing {} URL(s) \n \033[0m".format(inFile,runs))
except:
	pass

if args['buildir'] is True:

	url_list = open(inFile, "r")
	try:
		buildir.BUILDIR().buildir_function(inUrl)
	except KeyboardInterrupt:
                pass
	except:

	#pythonic way to count the number of URLs in a file
#	for site_url in url_list:
#		url = site_url.split()
#		num_urls += 1
		print("\033[92mRunning BuilDir to Create Archives\n \033[0m")
		buildir.BUILDIR().dir_builder(url_list, runs)
		url_list.close()
	print("\033[97m(+) DONE\n\033[0m")
if args['tumbleweed'] is True:
	getoutput("rm upSites.txt downSites.txt 2> /dev/null")
        scanList = open("upSites.txt", "a")
        downList = open("downSites.txt", "a")
	url_list = open(inFile, "r")
	try:
		print( "\033[092m\nRunning Tumbleweed Pre-scan \033[0m")
		tumbleweed.CURL_SWEEP().curl_sweeper(url_list,runs,scanList,downList)
		sys.stdout.write('\n')
        except KeyboardInterrupt:
                pass
	except:
		tumbleweed.CURL_SWEEP().curler(inUrl,scanList,downList)
	print("\033[97m(+) DONE\n\033[0m")

if args['squeal'] is True:
	print("\033[92mRunning Squeal:The Site-change Alerter \n \033[0m")
	print("\033[96m**site hashing takes an average of two minutes per site.Hang tight!**\033[0m")
	url_list = open(inFile, "r")
	try:
		squeal.WGET_RECURSE().wget_looper(url_list,runs)
               	sys.stdout.write("\n")
	except KeyboardInterrupt:
               pass

