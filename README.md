<p align="center" style="width:400px"><img src="https://github.com/Sean-Donnelly/lariat/blob/master/logo.PNG" style="width:400px"></p>
 
---

The Lariat toolset is a compilation of Python scripts used for gathering, updating, and organizing information to aid in web vulnerability scanning at scale

Tools
=====
* BuilDir - creates a file structure for sites to store changelog, index, and fingerprint files.  
  *   Checks if the changelogs, summaries, and indexes directories exist in the specified path; if not, creates them.  Then for each URL passed to BuilDir, creates a changelog, summary, and index file if they do not exist.  
* Tumbleweed - determines URL status, gathers site information (whois pull function in progress), creates a list of down sites and up sites, updates fingerprint files (.html files with site info and javascript graphs in progress), and creates a list of sites to scan.
* Squeal - uses stored index files to determine site changes and writes changes to changelogs.
  *   Continues as long as necessary directories exist and warns if otherwise before quitting.  Using multiprocessing, wgets each page of a site, hashes the files, delete the site directory, and compares the file hashes to results of a previous iteration.     
* Autoscan (in progress) - accepts a list of up sites that have changed to notify site owners and commence scanning with Netsparker, HPWebinspect and/or Acunetix.  Parses results to a product report template to be QC'd by the team before release.

Additional Info
===============
I created Lariat to address a list of issues identified within my security team.  

I wanted to:
* store and organize data in a way that was lightweight and easily searchable.  Although we scanned over a thousand different websites a year, we did not have a centralized archive containing information about the sites, previous scans results, etc.
* significantly decrease the number of scans we were conducting that would ultimately fail.  Every week we would attempt a certain amount of scans with about a 75% success rate.  
* drastically increase our scan rate.  At the time, for the most part we were scanning a site once per year.  My goal was to create an iterative cycle where every site was scanned at least four times per year and any time significant site changes were made.
* close or eliminate the communication gap between my security team and site owners.  Often times a website would undergo a significant change without my team being made aware, potentially introducing new attack vectors unbeknownst to anyone. I ultimately decided that making the determination ourself was the most reliable method and thus Squeal was created.
* automate the systematic parts of my team's workflow to allow them to spend more time producing quality reports.   
