#!/usr/bin/env python

import os
import re
import solr
import urllib
import zipfile

# grab the lcsh file if necessary
if (not os.path.isfile("lcsh.nt.zip")):
    os.system("wget http://id.loc.gov/static/data/lcsh.nt.zip")

# connect to solr
solr = solr.SolrConnection("http://localhost:8983/solr")

# open up the zip file
files = zipfile.ZipFile("lcsh.nt.zip")
nt_file = files.namelist()[0]

# regex out the pref label and concept uris
pref_label_pattern = r'^<(.+?)> <http://www.w3.org/2004/02/skos/core#prefLabel> "(.+)"@en.$'

# send the data off to solr
for l in files.open(nt_file):
    match = re.match(pref_label_pattern, l)
    if match: 
        uri, label = match.groups()
        solr.add(id=uri, label=label)
        print uri, label

solr.commit()
