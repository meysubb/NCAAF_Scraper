=============================
NCAA Football Stats Scraper

Author: Meyappan (Edited code by Rodrigo Zamith)

The initial script structure was written by Rodrigo Zamith for NCAA basketball. 

I made changes to his script recently when using it for other projects focusing on college baseball and basketball. For some recent projects, I used the exact structure that Rodrigo used to scrape NCAA football data. Lucikly, the NCAA website has the same structure for all sports!

I was interested in figuring out overall team stats, as well as individual game stats and results. The following scripts are included in this repository: 

1. create_team_mappings.py
2. create_schedule_mappings.py
3. create_overall_team_stats.py
4. ind_game_data.py  (stats for individual games)
5. ind_game_score.py (score for individual games)
6. season_team_data.py (seasonal average stats)

Version: 1.3

=============================

=============================
Author: Rodrigo Zamith  
Version: 1.1


Usage
-----
First, edit the scraper settings in `scrapersettings.py`. In particular, be sure to change the two variables at the top, `academic_year` and `year_index`, using the information provided in that file. You can also set what kind of data you'd like saved, and where you'd like it saved.

Then, execute either `ncaab_stats_scraper.sh` or `ncaab_stats_scraper.bat`, depending on your operating system. Alternatively, you can just execute the python files, preferably in this order:

1. create_team_mappings.py
2. create_schedule_mappings.py
3. create_player_mappings_and_agg_stats.py
4. create_ind_stats.py


Requirements
------------
This script requires Python, as well as the urllib2 and BeautifulSoup libraries.


License
--------
This script is licensed under the Mozilla Public License Version 2.0 (see LICENSE file in root folder). TL;DR: feel free to use it commercially, modify it, and distribute it, provided you disclose both the source code and any modifications you make to it.