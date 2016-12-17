import scraperfunctions
import scrapersettings
import csv
import re
from bs4 import BeautifulSoup

if (scrapersettings.summary_teams == 1):
    summary_team_data_w = open(scrapersettings.summary_team_data, "w")
    summary_team_data_w.writelines("team_id\tteam_name\tteam_games\tNet_Rush_Yds\tPass_Yds\tTot_Off\tPlays\tYds_Per_Play\tFirst_Downs_By_Penalty\tPenalties\tPenalties_Per_Game\tPenalties_Yds_Per_Game\tTot_Off_Yards_Per_Game\topp_team_games\topp_Net_Rush_Yds\topp_Pass_Yds\topp_Tot_Off\topp_Plays\topp_Yds_Per_Play\topp_First_Downs_By_Penalty\topp_Penalties\topp_Penalties_Per_Game\topp_Penalties_Yds_Per_Game\topp_Tot_Off_Yards_Per_Game\n")

    team_mapping = scraperfunctions.get_team_mappings()
    team_stats_total = []

    for value, team in enumerate(team_mapping):
        print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
        team_name = team_mapping[team][0]
        url = str(scrapersettings.domain_base) + "/team/" + team + "/stats?id=" + str(scrapersettings.year_index) 
        team_mainpage_data = scraperfunctions.grabber(url,scrapersettings.params, scrapersettings.http_header)
        team_mainpage_data_soup = BeautifulSoup(team_mainpage_data)
        # Get Correct Url for the Total Stats Category ID 
        # The total offense has defensive stats too, because your opponent totals is a sum of 
        # what your defense has allowed per game agaisnt you
        link = team_mainpage_data_soup.findAll("a",href=True, text='Total Offense')
        href_url = [x.get("href") for x in link]
        regexp = re.compile("year_stat_category_id=(.*)$")
        cat_id = regexp.search(href_url[0]).group(1)
        # New url
        new_url = url + "&year_stat_category_id=" + cat_id 
        team_tot_data = scraperfunctions.grabber(new_url,scrapersettings.params, scrapersettings.http_header)
        team_tot_data_soup = BeautifulSoup(team_tot_data)
        stat_grid = team_tot_data_soup.select('#stat_grid')

        team_tds = stat_grid[0].find('tfoot').findAll('tr')[1].findAll('td')
        team_games = str(team_tds[6].get_text().encode('utf-8').strip())
        team_rush_net_yds = str(team_tds[7].get_text().encode('utf-8').strip())
        #team_TOP = str(team_tds[8].get_text().encode('utf-8').strip())
        team_pass_yds = str(team_tds[9].get_text().encode('utf-8').strip())
        team_tot_off = str(team_tds[10].get_text().encode('utf-8').strip())
        team_plays = str(team_tds[11].get_text().encode('utf-8').strip())
        team_yds_per_play = str(team_tds[12].get_text().encode('utf-8').strip())
        team_first_downs_penalty = str(team_tds[15].get_text().encode('utf-8').strip())
        team_pens = str(team_tds[16].get_text().encode('utf-8').strip())
        team_pens_g = str(team_tds[17].get_text().encode('utf-8').strip())
        team_pens_yds_g = str(team_tds[19].get_text().encode('utf-8').strip())
        team_tot_off = str(team_tds[20].get_text().encode('utf-8').strip())

        team_stats  = [team_games,team_rush_net_yds,team_pass_yds,team_tot_off,team_plays,team_yds_per_play,team_first_downs_penalty,team_pens,team_pens_g,team_pens_yds_g,team_tot_off]

        opp_team_tds  = stat_grid[0].find('tfoot').findAll('tr')[1].findAll('td')
        opp_team_games = str(opp_team_tds[6].get_text().encode('utf-8').strip())
        opp_team_rush_net_yds = str(opp_team_tds[7].get_text().encode('utf-8').strip())
        #team_TOP = str(team_tds[8].get_text().encode('utf-8').strip())
        opp_team_pass_yds = str(opp_team_tds[9].get_text().encode('utf-8').strip())
        opp_team_tot_off = str(opp_team_tds[10].get_text().encode('utf-8').strip())
        opp_team_plays = str(opp_team_tds[11].get_text().encode('utf-8').strip())
        opp_team_yds_per_play = str(opp_team_tds[12].get_text().encode('utf-8').strip())
        opp_team_first_downs_penalty = str(opp_team_tds[15].get_text().encode('utf-8').strip())
        opp_team_pens = str(opp_team_tds[16].get_text().encode('utf-8').strip())
        opp_team_pens_g = str(opp_team_tds[17].get_text().encode('utf-8').strip())
        opp_team_pens_yds_g = str(opp_team_tds[19].get_text().encode('utf-8').strip())
        opp_team_tot_off = str(opp_team_tds[20].get_text().encode('utf-8').strip())

        opp_team_stats  = [opp_team_games,opp_team_rush_net_yds,opp_team_pass_yds,opp_team_tot_off,opp_team_plays,opp_team_yds_per_play,opp_team_first_downs_penalty,opp_team_pens,opp_team_pens_g,opp_team_pens_yds_g,opp_team_tot_off]
        team_stats_total = [team, team_name] + team_stats + opp_team_stats

        if (scrapersettings.summary_teams == 1):
            writeline = ""
            for item in team_stats_total:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            summary_team_data_w.writelines(writeline)




