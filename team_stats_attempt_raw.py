import scraperfunctions
import scrapersettings
import csv
import re
from bs4 import BeautifulSoup

if (scrapersettings.summary_teams == 1):

    summary_team_data_w = open(scrapersettings.summary_team_data, "w")

    team_mapping = scraperfunctions.get_team_mappings()
    team_stats_total = []
    headers = 0
    for value, team in enumerate(team_mapping):
        print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
        team_name = team_mapping[team][0]
        ## Base url - hits rushing page

        ### Note just write a function that does everything below and then loop over it for the
        ### different categories, rushing, passing, etc.
        url = str(scrapersettings.domain_base) + "/team/" + team + "/stats?id=" + str(scrapersettings.year_index)
        team_mainpage_data = scraperfunctions.grabber(url,scrapersettings.params, scrapersettings.http_header)
        team_mainpage_data_soup = BeautifulSoup(team_mainpage_data)


        first_page_rush = team_mainpage_data_soup.select('#stat_grid')

        ### Create headers for tsv file.
        if(headers==0):
            headers_raw = first_page_rush[0].findAll('th')
            headers = [item.get_text().encode('utf-8').strip() for item in headers_raw]
            opp_headers = [("opp_" + str(item)) for item in headers]
            all_headers_raw = headers + opp_headers
            all_headers_raw2 = [x.replace(" ", "_") for x in all_headers_raw]
            all_headers_final = [x.replace("/", "_per_") for x in all_headers_raw2]
            all_headers_final[0] = 'team_id'
            all_headers_final[1] = 'team_name'
            if (scrapersettings.summary_teams == 1):
                writeline = ""
                for item in all_headers_final:
                    writeline += str(item) + "\t"
                writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                summary_team_data_w.writelines(writeline)

        ## First page raw - rushing data (team and opponent)
        tot_raw = first_page_rush[0].find('tfoot').findAll('tr')[1].findAll('td')
        tot_raw = [item.get_text().encode('utf-8').strip() for item in tot_raw]
        tot_f = [x.replace("-", "0").replace(",", "") for x in tot_raw]
        opp_raw = first_page_rush[0].find('tfoot').findAll('tr')[2].findAll('td')
        opp_raw = [item.get_text().encode('utf-8').strip() for item in opp_raw]
        opp_f = [x.replace("-", "0").replace(",", "") for x in opp_raw]

        tot_f[0] = team
        tot_f[1] = team_name
        team_stats_total = tot_f + opp_f

        if (scrapersettings.summary_teams == 1):
            writeline = ""
            for item in team_stats_total:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            summary_team_data_w.writelines(writeline)
