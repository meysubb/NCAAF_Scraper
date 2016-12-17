# Import modules and libraries
import scraperfunctions
import scrapersettings
import csv
import re
import requests
import json
from bs4 import BeautifulSoup

if (scrapersettings.ind_game_stats == 1):
    # Create the file headings
    game_data_w = open(scrapersettings.game_data, "w")
    game_data_w.writelines("game_id\taway_team_id\taway_team\taway_first_downs\taway_passing_first_downs\taway_rushing_first_downs\taway_rushing_yds\taway_rushing_attempts\taway_passing_attempts\taway_passing_completions\taway_passing_interceptions\taway_avg_per_pass\t away_pass_yds\taway_yds_per_play\taway_tot_offense\taway_fumbles_number\taway_fumbles_lost\taway_pen_number\taway_pen_yds\taway_pun_number\taway_pun_yds\taway_pun_re_number\taway_pun_re_yds\taway_kick_re_number\taway_kick_re_yds\taway_int_re_number\taway_int_re_yds\taway_third_down_attempts\taway_third_down_suc\taway_fourth_down_attempts\taway_fourth_down_suc\thome_team_id\thome_team\thome_first_downs\thome_passing_first_downs\thome_rushing_first_downs\thome_rushing_yds\thome_rushing_attempts\thome_passing_attempts\thome_passing_completions\thome_passing_interceptions\thome_avg_per_pass\t home_pass_yds\thome_yds_per_play\thome_tot_offense\thome_fumbles_number\thome_fumbles_lost\thome_pen_number\thome_pen_yds\thome_pun_number\thome_pun_yds\thome_pun_re_number\thome_pun_re_yds\thome_kick_re_number\thome_kick_re_yds\thome_int_re_number\thome_int_re_yds\thome_third_down_attempts\thome_third_down_suc\thome_fourth_down_attempts\thome_fourth_down_suc\n")

game_mapping = scraperfunctions.get_game_mappings()

for value, game in enumerate(game_mapping):
    if scrapersettings.debugmode == 1: 
         print "Processing game " + str(game) + " (" + str(value+1) + " of " + str(len(game_mapping)) + ")"
        # Adjust url to get background json data
         game_url = game_mapping[game][4]
         sep = '#'
         game_url = game_url.split(sep, 1)[0] + "/team-stats"
         extract = re.search('.com/(.*)/team-stats', game_url)
         url_json = 'http://data.ncaa.com/jsonp/' + extract.group(1) + '/teamStats.json'
        # Convert JSONP string to JSON to dictionary in python
         r = requests.get(url_json)
         if(r.status_code == 404):
            continue
         s = str(r.text)
         s = s.replace(';', '')
         apijson = s[ s.index("(") + 1 : s.rindex(")") ]
         json_val = json.loads(apijson)

         first_team = str(json_val['meta']['teams'][0]['homeTeam'])
         second_team = str(json_val['meta']['teams'][1]['homeTeam'])
         if(first_team == 'false'): 
             away_team = json_val['meta']['teams'][0]['shortname']
             away_team_id = json_val['meta']['teams'][0]['id']
         elif(first_team == 'true'):
             home_team = json_val['meta']['teams'][0]['shortname']
             home_team_id = json_val['meta']['teams'][0]['id']

         if(second_team == 'true'):
             home_team = json_val['meta']['teams'][1]['shortname']
             home_team_id = json_val['meta']['teams'][1]['id']
         elif(second_team == 'false'):
             away_team = json_val['meta']['teams'][1]['shortname']
             away_team_id = json_val['meta']['teams'][1]['id']

         teamId_1 = json_val['teams'][0]['teamId']
         teamId_2 = json_val['teams'][1]['teamId']


         if(teamId_1 == away_team_id):
             away_first_downs = json_val['teams'][0]['stats'][0]['data']
             away_passing_first_downs = json_val['teams'][0]['stats'][0]['breakdown'][0]['data']
             away_rushing_first_downs = json_val['teams'][0]['stats'][0]['breakdown'][1]['data']
             away_rushing_yds = json_val['teams'][0]['stats'][1]['data']
             away_rushing_attempts = json_val['teams'][0]['stats'][1]['breakdown'][0]['data']
             away_rushing_avg_per_rush = json_val['teams'][0]['stats'][1]['breakdown'][1]['data']
             away_passing_attempts = json_val['teams'][0]['stats'][2]['breakdown'][0]['data']
             away_passing_completions = json_val['teams'][0]['stats'][2]['breakdown'][1]['data']
             away_passing_interceptions = json_val['teams'][0]['stats'][2]['breakdown'][2]['data']
             away_avg_per_pass = json_val['teams'][0]['stats'][2]['breakdown'][3]['data']
             away_pass_yds = json_val['teams'][0]['stats'][2]['data']
             away_off_plays = json_val['teams'][0]['stats'][3]['breakdown'][0]['data']
             away_yds_per_play = json_val['teams'][0]['stats'][3]['breakdown'][1]['data']
             away_tot_offense = json_val['teams'][0]['stats'][3]['data']
             away_fumbs = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][4]['data']))
             away_fumbles_number = away_fumbs[0]
             away_fumbles_lost = away_fumbs[1]
             away_pen = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][5]['data']))
             away_pen_number = away_pen[0]
             away_pen_yds = away_pen[1]
             away_avg_punt = json_val['teams'][0]['stats'][6]['breakdown'][0]['data']
             away_pun = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][6]['data']))
             away_pun_number = away_pun[0]
             away_pun_yds = away_pun[1]
             away_pun_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][7]['data']))
             away_pun_re_number = away_pun_re[0]
             away_pun_re_yds = away_pun_re[1]
             away_kick_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][8]['data']))
             away_kick_re_number = away_kick_re[0]
             away_kick_re_yds = away_kick_re[1]
             away_int_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][9]['data']))
             away_int_re_number = away_int_re[0]
             away_int_re_yds = away_int_re[1]
             away_third_down_conv = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][10]['data']))
             away_third_down_suc = away_third_down_conv[0]
             away_third_down_attempts = away_third_down_conv[1]
             away_fourth_down_conv = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][11]['data']))
             away_fourth_down_suc = away_fourth_down_conv[0]
             away_fourth_down_attempts = away_fourth_down_conv[1]
         else: 
             home_first_downs = json_val['teams'][0]['stats'][0]['data']
             home_passing_first_downs = json_val['teams'][0]['stats'][0]['breakdown'][0]['data']
             home_rushing_first_downs = json_val['teams'][0]['stats'][0]['breakdown'][1]['data']
             home_rushing_yds = json_val['teams'][0]['stats'][1]['data']
             home_rushing_attempts = json_val['teams'][0]['stats'][1]['breakdown'][0]['data']
             home_rushing_avg_per_rush = json_val['teams'][0]['stats'][1]['breakdown'][1]['data']
             home_passing_attempts = json_val['teams'][0]['stats'][2]['breakdown'][0]['data']
             home_passing_completions = json_val['teams'][0]['stats'][2]['breakdown'][1]['data']
             home_passing_interceptions = json_val['teams'][0]['stats'][2]['breakdown'][2]['data']
             home_avg_per_pass = json_val['teams'][0]['stats'][2]['breakdown'][3]['data']
             home_pass_yds = json_val['teams'][0]['stats'][2]['data']['data']
             home_off_plays = json_val['teams'][0]['stats'][3]['breakdown'][0]['data']
             home_yds_per_play = json_val['teams'][0]['stats'][3]['breakdown'][1]['data']
             home_tot_offense = json_val['teams'][0]['stats'][3]['data']
             home_fumbs = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][4]['data']))
             home_fumbles_number = home_fumbs[0]
             home_fumbles_lost = home_fumbs[1]
             home_pen = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][5]['data']))
             home_pen_number = home_pen[0]
             home_pen_yds = home_pen[1]
             home_avg_punt = json_val['teams'][0]['stats'][6]['breakdown'][0]['data']
             home_pun = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][6]['data']))
             home_pun_number = home_pun[0]
             home_pun_yds = home_pun[1]
             home_pun_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][7]['data']))
             home_pun_re_number = home_pun_re[0]
             home_pun_re_yds = home_pun_re[1]
             home_kick_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][8]['data']))
             home_kick_re_number = home_kick_re[0]
             home_kick_re_yds = home_kick_re[1]
             home_int_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][9]['data']))
             home_int_re_number = home_int_re[0]
             home_int_re_yds = home_int_re[1]
             home_third_down_conv = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][10]['data']))
             home_third_down_suc = home_third_down_conv[0]
             home_third_down_attempts = home_third_down_conv[1]
             home_fourth_down_conv = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][11]['data']))
             home_fourth_down_suc = home_fourth_down_conv[0]
             home_fourth_down_attempts = home_fourth_down_conv[1]

         if(teamId_2 == away_team_id): 
             away_first_downs = json_val['teams'][1]['stats'][0]['data']
             away_passing_first_downs = json_val['teams'][1]['stats'][0]['breakdown'][0]['data']
             away_rushing_first_downs = json_val['teams'][1]['stats'][0]['breakdown'][1]['data']
             away_rushing_yds = json_val['teams'][1]['stats'][1]['data']
             away_rushing_attempts = json_val['teams'][1]['stats'][1]['breakdown'][0]['data']
             away_rushing_avg_per_rush = json_val['teams'][1]['stats'][1]['breakdown'][1]['data']
             away_passing_attempts = json_val['teams'][1]['stats'][2]['breakdown'][0]['data']
             away_passing_completions = json_val['teams'][1]['stats'][2]['breakdown'][1]['data']
             away_passing_interceptions = json_val['teams'][1]['stats'][2]['breakdown'][2]['data']
             away_avg_per_pass = json_val['teams'][1]['stats'][2]['breakdown'][3]['data']
             away_pass_yds = json_val['teams'][1]['stats'][2]['data']
             away_yds_per_play = json_val['teams'][1]['stats'][3]['breakdown'][1]['data']
             away_tot_offense = json_val['teams'][1]['stats'][3]['data']
             away_fumbs = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][4]['data']))
             away_fumbles_number = away_fumbs[0]
             away_fumbles_lost = away_fumbs[1]
             away_pen = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][5]['data']))
             away_pen_number = away_pen[0]
             away_pen_yds = away_pen[1]
             away_avg_punt = json_val['teams'][1]['stats'][6]['breakdown'][0]['data']
             away_pun = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][6]['data']))
             away_pun_number = away_pun[0]
             away_pun_yds = away_pun[1]
             away_pun_re = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][7]['data']))
             away_pun_re_number = away_pun_re[0]
             away_pun_re_yds = away_pun_re[1]
             away_kick_re = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][8]['data']))
             away_kick_re_number = away_kick_re[0]
             away_kick_re_yds = away_kick_re[1]
             away_int_re = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][9]['data']))
             away_int_re_number = away_int_re[0]
             away_int_re_yds = away_int_re[1]
             away_third_down_conv = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][10]['data']))
             away_third_down_suc = away_third_down_conv[0]
             away_third_down_attempts = away_third_down_conv[1]
             away_fourth_down_conv = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][11]['data']))
             away_fourth_down_suc = away_fourth_down_conv[0]
             away_fourth_down_attempts = away_fourth_down_conv[1]
         else:
             home_first_downs = json_val['teams'][1]['stats'][0]['data']
             home_passing_first_downs = json_val['teams'][1]['stats'][0]['breakdown'][0]['data']
             home_rushing_first_downs = json_val['teams'][1]['stats'][0]['breakdown'][1]['data']
             home_rushing_yds = json_val['teams'][1]['stats'][1]['data']
             home_rushing_attempts = json_val['teams'][1]['stats'][1]['breakdown'][0]['data']
             home_rushing_avg_per_rush = json_val['teams'][1]['stats'][1]['breakdown'][1]['data']
             home_passing_attempts = json_val['teams'][1]['stats'][2]['breakdown'][0]['data']
             home_passing_completions = json_val['teams'][1]['stats'][2]['breakdown'][1]['data']
             home_passing_interceptions = json_val['teams'][1]['stats'][2]['breakdown'][2]['data']
             home_avg_per_pass = json_val['teams'][1]['stats'][2]['breakdown'][3]['data']
             home_pass_yds = json_val['teams'][1]['stats'][2]['data']
             home_yds_per_play = json_val['teams'][1]['stats'][3]['breakdown'][1]['data']
             home_tot_offense = json_val['teams'][1]['stats'][3]['data']
             home_fumbs = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][4]['data']))
             home_fumbles_number = home_fumbs[0]
             home_fumbles_lost = home_fumbs[1]
             home_pen = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][5]['data']))
             home_pen_number = home_pen[0]
             home_pen_yds = home_pen[1]
             home_avg_punt = json_val['teams'][1]['stats'][6]['breakdown'][0]['data']
             home_pun = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][6]['data']))
             home_pun_number = home_pun[0]
             home_pun_yds = home_pun[1]
             home_pun_re = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][7]['data']))
             home_pun_re_number = home_pun_re[0]
             home_pun_re_yds = home_pun_re[1]
             home_kick_re = re.split(r'[\s-]+', str(json_val['teams'][0]['stats'][8]['data']))
             home_kick_re_number = home_kick_re[0]
             home_kick_re_yds = home_kick_re[1]
             home_int_re = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][9]['data']))
             home_int_re_number = home_int_re[0]
             home_int_re_yds = home_int_re[1]
             home_third_down_conv = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][10]['data']))
             home_third_down_suc = home_third_down_conv[0]
             home_third_down_attempts = home_third_down_conv[1]
             home_fourth_down_conv = re.split(r'[\s-]+', str(json_val['teams'][1]['stats'][11]['data']))
             home_fourth_down_suc = home_fourth_down_conv[0]
             home_fourth_down_attempts = home_fourth_down_conv[1]

         home_team_stats = [home_team_id,home_team,home_first_downs,home_passing_first_downs,home_rushing_first_downs,home_rushing_yds,home_rushing_attempts,home_passing_attempts,home_passing_completions,home_passing_interceptions,home_avg_per_pass, home_pass_yds,home_yds_per_play,home_tot_offense,home_fumbles_number,home_fumbles_lost,home_pen_number,home_pen_yds,home_pun_number,home_pun_yds,home_pun_re_number,home_pun_re_yds,home_kick_re_number,home_kick_re_yds,home_int_re_number,home_int_re_yds,home_third_down_attempts,home_third_down_suc,home_fourth_down_attempts,home_fourth_down_suc]

         away_team_stats = [away_team_id,away_team,away_first_downs,away_passing_first_downs,away_rushing_first_downs,away_rushing_yds,away_rushing_attempts,away_passing_attempts,away_passing_completions,away_passing_interceptions,away_avg_per_pass, away_pass_yds,away_yds_per_play,away_tot_offense,away_fumbles_number,away_fumbles_lost,away_pen_number,away_pen_yds,away_pun_number,away_pun_yds,away_pun_re_number,away_pun_re_yds,away_kick_re_number,away_kick_re_yds,away_int_re_number,away_int_re_yds,away_third_down_attempts,away_third_down_suc,away_fourth_down_attempts,away_fourth_down_suc]

         total_team_stats = [game] + away_team_stats + home_team_stats


         if (scrapersettings.ind_game_stats == 1):
          writeline = ""
          for item in total_team_stats:
              writeline += str(item) + "\t"
          #writeline = re.sub('\t$', '', writeline)            
          writeline += "\n"
          game_data_w.writelines(writeline)
