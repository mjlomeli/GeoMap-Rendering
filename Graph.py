import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
from plotly.graph_objs import Bar, Layout
import numpy as np
import pandas as pd
import random
import csv
import time
import display
from collections import OrderedDict
from pathlib import Path
random.seed(time.clock())
plotly.tools.set_credentials_file(username='mauricio.jr.lomeli', api_key='TEhCAdafmpsAJ3K0h4Ll')

class graph:
    def __init__(self):
        self.__setUnemploymentRate()
        
    def __setUnemploymentRate(self):
        try:
            dat = []
            with open('dont_change_anything.csv', 'r') as r:
                reader = csv.DictReader(r)
                headers = reader.fieldnames
                dat = list(reader)
            if dat != None and len(dat) != 0:
                with open('dont_change_anything.csv', 'w', newline='') as w:
                    writer = csv.DictWriter(w, headers)
                    writer.writeheader()
                    with open('import_data_here.csv', 'r') as j:
                        reader = csv.DictReader(j)
                        data = list(reader)
                        for my_d in dat:
                            for my_dict in data:
                                if my_dict['State FIPS Code'] == my_d['State FIPS Code']:
                                    if random.random() > random.random():
                                        my_d['Unemployment Rate'] = my_dict['Unemployment Rate'] + random.random()
                                    else:
                                        my_d['Unemployment Rate'] = my_dict['Unemployment Rate'] - random.random()
                                    writer.writerow(my_d)
            else:
                self.__check()
        except:
            self.__check()

    def __check(self):
        backup = Path(Path.cwd()) / Path('Backups') / Path('dont_change_anything.csv')
        with open(backup, 'r') as r:
            reader = csv.DictReader(r)
            headers = reader.fieldnames
            data = list(reader)
        with open('dont_change_anything.csv', 'w', newline='') as w:
            writer = csv.DictWriter(w, headers)
            writer.writeheader()
            for my_dict in data:
                writer.writerow(my_dict)

    def usa(self, graphNum=0):
        df_sample = pd.read_csv('dont_change_anything.csv')
        df_sample['State FIPS Code'] = df_sample['State FIPS Code'].apply(lambda x: str(x).zfill(2)) #fills front of integer with zeros
        df_sample['County FIPS Code'] = df_sample['County FIPS Code'].apply(lambda x: str(x).zfill(3)) #fills front of integer with zeros
        df_sample['FIPS'] = df_sample['State FIPS Code'] + df_sample['County FIPS Code'] #concatenating the strings is the id for location of the county (like a 2d array)
        if graphNum == 0:
            colorscale = ["#ffff66","#ffff4d","#ffff1a","#ffff00","#e6e600","#cccc00", "#b3b300", "#999900",
                        "#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9", "#08519c","#0b4083","#08306b"]
        elif graphNum == 1:
            colorscale = ['#4000ff', '#0000ff', '#0040ff', '#0080ff', '#00bfff', '#00ffff', '#00ffbf', '#00ff80', 
                          '#00ff40', '#00ff00', '#40ff00', '#80ff00', '#bfff00', '#ffff00', '#ffbf00', '#ff8000', 
                          '#ff4000', '#ff0000']


#ff0000
#ff4000
#ff8000	
#ffbf00	
#ffff00	
#bfff00	
#80ff00	
#40ff00	
#00ff00	
#00ff40	
#00ff80	
#00ffbf	
#00ffff	
#00bfff	
#0080ff	
#0040ff	

#4000ff #0000ff	#0040ff	#0080ff	#00bfff	#00ffff	#00ffbf	#00ff80	#00ff40	#00ff00	#40ff00	#80ff00	#bfff00	#ffff00	#ffbf00	#ff8000	#ff4000 #ff0000




    
        ###################################################
        ### change 1 and 12 for the range of colors. ######
        endpts = list(np.linspace(0, 8, len(colorscale) - 1))  #creates the legend ranges
        fips = df_sample['FIPS'].tolist()
        values = df_sample['Unemployment Rate'].tolist()
        
        fig = ff.create_choropleth(
            fips=fips, values=values,
            binning_endpoints=endpts,
            colorscale=colorscale,
            show_state_data=False,
            show_hover=True, centroid_marker={'opacity': 0},
            asp=2.9, title='USA by Unemployment',
            legend_title='Unemployment'
        
        )
        return fig
        #py.iplot(fig, filename='choropleth_full_usa')

    def basic(self,title='title', fieldnames=['field1, field2'], values=[1,2]):
        """
        Example:
        basic("The Title", ["Bar_1", "Bar_2"],[1,2])
        """
        
        data = [plotly.graph_objs.Bar(
                x=fieldnames,
                y=values
        )]
        layout = plotly.graph_objs.Layout(title=title)
        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        #plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))
        return fig

    def stacked(self,title='title', dictList= [OrderedDict([('groupName','gname'), ('values',1), ('barName','Barname')])]):
        #dictList is a LIST of Dictionaries
        data = list()
        for my_dict in dictList:
            data.append(plotly.graph_objs.Bar(
                x=my_dict['groupName'],
                y=my_dict['values'],
                name=my_dict['barName']
            ))
        layout = plotly.graph_objs.Layout(
            barmode='stack', 
            title=title)
        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        #plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))
        return fig

    def grouped(self, title='title', dictList= [OrderedDict([('groupName','gname'), ('values',1), ('barName','Barname')])]):
        data = list()
        for my_dict in dictList:
            data.append(Bar(
                x=my_dict['groupName'],
                y=my_dict['values'],
                name=my_dict['barName']
            ))
    
        layout = plotly.graph_objs.Layout(barmode='group', title=title)
        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        #plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))
        return fig

COLORS = ['rgb(114,90,193)', 'rgb(128,206,215)', 'rgb(0,121,214)', 'rgb(173,10,101)']

def playerstats(team_id, conn, curr, player_position):
    find_players = """
    SELECT user_id FROM Teams
    WHERE team_id=?
    """
    curr.execute(find_players, (team_id,))
    teammates = curr.fetchall()

    user_id = teammates[player_position][0]

    cmd = """
    SELECT event_id, kills, headshots, damage, distance FROM Playerstats
    WHERE user_id=?
    """
    curr.execute(cmd, (user_id,))
    stats = curr.fetchall()

    player_dict = {}
    data = []
    partitions = ['Kills', 'Headshots', 'Damage', 'Distance']
    title = 'Point Breakdown for Player {}'.format(user_id)
    for event in stats:
        event_id = event[0]
        kills = event[1]
        headshots = event[2]
        damage = event[3]
        distance = event[4]
        player_dict[event_id] = [kills * 1000, headshots * 1000, damage, distance]
    
    color_index = 0
    for event, stats in player_dict.items():
        data.append(
            Bar(
                x=partitions,
                y=stats,
                name='Event {}'.format(event),
                marker=dict(
                    color=COLORS[color_index]
                )
            )
        )
        color_index += 1

    layout = Layout(
        barmode='group',
        title=title,
        yaxis=dict(
            title='Points'
        ),
        xaxis=dict(
            title='Point Breakdown'
        )
    )
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    return fig


def teamstats(team_id, conn, curr):
    """
    Use this function by adding the team_id as the argument. It can be done in
    a number of ways:

    teamstats(3)      #can take one user id
    teamstats([2,3])  #or can run multiple user ids

    """
    
    title = "Team Points Breakdown for Team {}".format(team_id)
    cmd = """
    SELECT user_id, event_id, team_id, score FROM PlayerStats
    WHERE team_id={}
    """.format(team_id)
    curr.execute(cmd)
    teamscores = curr.fetchall()
    player_dict = {}
    event_set = set()
    data = []
    for player in teamscores:
        user_id = player[0]
        event_id = player[1]
        score = player[3]
        if user_id in player_dict:
            player_dict[user_id][event_id] = score
        else:
            player_dict[user_id] = {event_id: score}
        event_set.add(event_id)

    color_index = 0
    for player, score in player_dict.items():
        scores = []
        for event_id in event_set:
            scores.append(player_dict[player][event_id])
        width = 0
        if len(event_set) == 1:
            data.append(
                Bar(
                    x=['event {}'.format(str(event_id)) for event_id in list(event_set)],
                    y=scores,
                    name='Player ID {}'.format(player),
                    width=.4,
                    marker=dict(
                        color=COLORS[color_index]
                    )
                )
            )
        else:
            data.append(
                Bar(
                    x=['event {}'.format(str(event_id)) for event_id in list(event_set)],
                    y=scores,
                    name='Player ID {}'.format(player),
                    marker=dict(
                        color=COLORS[color_index]
                    )
                )
            )
        color_index += 1

    layout = Layout(
        barmode='stack',
        title=title,
        yaxis=dict(
            title='Points'
        ),
        xaxis=dict(
            title='Events'
        )
    )
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    return fig




def my_dict(x,y,z):
    return OrderedDict([('groupName', x), ('values', y), ('barName', z)])

def main():
    display.run_dash()





if __name__ == '__main__':
    main()