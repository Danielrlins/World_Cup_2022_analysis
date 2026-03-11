from statsbombpy import sb
import pandas as pd

def load_world_cup_2022():

    competitions = sb.competitions()

    wc_2022 = competitions[
        (competitions['competition_name'] == 'FIFA World Cup') &
        (competitions['season_name'] == '2022')
    ]

    matches = sb.matches(
        competition_id=wc_2022.iloc[0]['competition_id'],
        season_id=wc_2022.iloc[0]['season_id']
    )

    matches['total_goals'] = matches['home_score'] + matches['away_score']
    matches['goal_difference'] = abs(matches['home_score'] - matches['away_score'])

    return matches


def create_team_table(matches):

    home = matches[['home_team','home_score','away_score']].copy()
    home.columns = ['team','goals_for','goals_against']

    away = matches[['away_team','away_score','home_score']].copy()
    away.columns = ['team','goals_for','goals_against']

    table = pd.concat([home, away])

    table['points'] = 0
    table.loc[table['goals_for'] > table['goals_against'], 'points'] = 3
    table.loc[table['goals_for'] == table['goals_against'], 'points'] = 1

    summary = table.groupby('team').agg(
        games=('team','count'),
        goals_for=('goals_for','sum'),
        goals_against=('goals_against','sum'),
        points=('points','sum')
    )

    summary['goal_diff'] = summary['goals_for'] - summary['goals_against']

    return summary.sort_values('points', ascending=False)

def get_goal_scorers(matches):

    all_goals = []

    for match_id in matches['match_id']:
        events = sb.events(match_id=match_id)

        goals = events[
            (events['type'] == 'Shot') &
            (events['shot_outcome'] == 'Goal')
        ]

        goal_data = goals[['player', 'team']].copy()
        all_goals.append(goal_data)

    all_goals = pd.concat(all_goals)

    scorers = (
        all_goals
        .groupby(['player','team'])
        .size()
        .reset_index(name='goals')
        .sort_values('goals', ascending=False)
    )

    return scorers
