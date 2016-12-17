# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
os.getcwd()
import scraperfunctions
import scrapersettings
import csv
import re
import requests 
import urllib2
import time
#from urllib.request import urlopen
from bs4 import BeautifulSoup

tstats = open(scrapersettings.tstats_data, "w")
tstats.writelines("team\tstats\trankings\tvalue\n")

record = open(scrapersettings.record_data,"w")
record.writelines("team\twin\tlosses\n")
    
team_mapping = scraperfunctions.get_team_mappings()


for value, team in enumerate(team_mapping):
    roster_url = str(scrapersettings.domain_base) + "/team/" + team + "/" + str(scrapersettings.year_index)
    team_name = team_mapping[team][0]
    if(team == '30'):
        continue 
    try: 
        #time.sleep(2)
        r = requests.get(roster_url)
        # , timeout=10
        r.raise_for_status()
        #ht = urlopen(roster_url)
        #except HTTPError
    except Exception:  
        roster_url = str(scrapersettings.domain_base) + "/team/" + team + "/" + str(scrapersettings.year_index) + "?game_sport_year_ctl_id=" + str(scrapersettings.year_index)
        #team_mainpage_data = scraperfunctions.grabber(roster_url,scrapersettings.params, scrapersettings.http_header)
    team_mainpage_data = scraperfunctions.grabber(roster_url,scrapersettings.params, scrapersettings.http_header)    
    team_mainpage_data_soup = BeautifulSoup(team_mainpage_data)
    table = team_mainpage_data_soup.findAll("table",{"class" : "mytable"})
    team_stats = []
    print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
    for rowno,row in enumerate(table[1].findAll("tr")):
        tds = row.findAll('td')
        if(len(tds) < 3):
            continue
        else:
            name = team_name
            stat = str(tds[0].get_text().encode('utf-8').strip())
            rank = str(tds[1].get_text().encode('utf-8').strip())#.get_text().encode('utf-8').strip()
            value = str(tds[2].get_text().encode('utf-8').strip())#.get_text().encode('utf-8').strip()
        table_stats = [name,stat,rank,value]
        team_stats.append(table_stats)
        if (scrapersettings.tstats == 1):
            writeline = ""
            for item in table_stats:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            tstats.writelines(writeline)
            
    name_record = team_mainpage_data_soup.find('span',{'class':'org_heading'})
    nr_text = name_record.get_text().encode('utf-8').strip()
    nr_split = re.split(r'[()]', nr_text)
    if(len(nr_split) == 5): 
        rec = re.split(r'[-]',nr_split[3])
    elif(len(nr_split) > 1):
        rec = re.split(r'[-]',nr_split[1])
    elif(len(nr_split) == 3): 
        rec = re.split(r'[-]',nr_split)
    w = rec[0]
    l = rec[1]
    record_stats = [team_name,w,l]
    if(scrapersettings.tstats == 1):
        wline = ""
        for item in record_stats:
            wline += str(item) + "\t"
        wline = re.sub('\t$', '', wline)
        wline += "\n"
        record.writelines(wline)
        
    