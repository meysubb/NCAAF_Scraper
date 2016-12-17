import scraperfunctions
import scrapersettings
import csv
import re
import requests
import json
from bs4 import BeautifulSoup

if (scrapersettings.ind_game_score == 1):
    # Create the file headings
    game_score_w = open(scrapersettings.game_score, "w")
    game_score_w.writelines("game_id\taway_team_name\taway_team_score\thome_team_name\thome_team_score\n")


game_mapping = scraperfunctions.get_game_mappings()

for value, game in enumerate(game_mapping):
    if scrapersettings.debugmode == 1: 
         print "Processing game " + str(game) + " (" + str(value+1) + " of " + str(len(game_mapping)) + ")"

         game_url = game_mapping[game][4]
         sep = '#'
         game_url = game_url.split(sep, 1)[0] + "/team-stats"
         extract = re.search('.com/(.*)/team-stats', game_url)
         url_json = 'http://data.ncaa.com/jsonp/' + extract.group(1) + '/gameinfo.json'

         # Convert JSONP string to JSON to dictionary in python
         r = requests.get(url_json)
         if(r.status_code == 404):
            continue
         s = r.text   
         s.encode('utf8')   
         try:
            s = str(s)
         except:
            continue
         s = s.replace(';', '')
         apijson = s[ s.index("(") + 1 : s.rindex(")") ]
         json_val = json.loads(apijson)

         away_team_name = json_val['away']['nameRaw']
         away_team_score = json_val['away']['currentScore']
         home_team_name = json_val['home']['nameRaw']
         home_team_score = json_val['home']['currentScore']

         home_team = [home_team_name, home_team_score]
         away_team = [away_team_name, away_team_score]

         total_team_stats = [game] + away_team + home_team

         if (scrapersettings.ind_game_score == 1):
              writeline = ""
              for item in total_team_stats:
                  writeline += str(item) + "\t"
              #writeline = re.sub('\t$', '', writeline)            
              writeline += "\n"
              game_score_w.writelines(writeline)
