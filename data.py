import requests
import pandas as pd
import os

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()

# building tables from endpoints
elements_df = pd.DataFrame(json['elements'])
element_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])

players_history = pd.DataFrame()
for p_id in elements_df['id']:
    url = 'https://fantasy.premierleague.com/api/element-summary/' + str(p_id)
    r = requests.get(url)

    json = r.json()

    history_past = pd.DataFrame(json['history_past'])
    history_past['id'] = p_id

    players_history = pd.concat([players_history, history_past])

elements_df['position'] = elements_df.element_type.map(element_types_df.set_index('id').singular_name)
elements_df['team'] = elements_df.team.map(teams_df.set_index('id').name)

players_history['position'] = players_history.id.map(elements_df.set_index('id').position)
players_history['team'] = players_history.id.map(elements_df.set_index('id').team)

elements_df.to_csv(os.path.join(os.path.curdir, 'data', 'curr_player_df.csv'))
players_history.to_csv(os.path.join(os.path.curdir, 'data', 'player_hist_df.csv'))