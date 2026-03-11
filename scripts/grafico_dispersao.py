import pandas as pd
import plotly.graph_objects as go
from statsbombpy import sb

# -----------------------------
# carregar jogos da copa 2022
# -----------------------------

matches = sb.matches(competition_id=43, season_id=106)

# -----------------------------
# criar dataframe com todos os times
# -----------------------------

data = []

for _, row in matches.iterrows():

    data.append({
        "team": row["home_team"],
        "goals_scored": row["home_score"],
        "goals_conceded": row["away_score"]
    })

    data.append({
        "team": row["away_team"],
        "goals_scored": row["away_score"],
        "goals_conceded": row["home_score"]
    })

df = pd.DataFrame(data)

# -----------------------------
# calcular médias
# -----------------------------

team_stats = df.groupby("team").agg({
    "goals_scored":"mean",
    "goals_conceded":"mean"
}).reset_index()

# -----------------------------
# código das bandeiras
# -----------------------------

iso_map = {
"Argentina":"ar",
"Australia":"au",
"Belgium":"be",
"Brazil":"br",
"Cameroon":"cm",
"Canada":"ca",
"Costa Rica":"cr",
"Croatia":"hr",
"Denmark":"dk",
"Ecuador":"ec",
"England":"gb",
"France":"fr",
"Germany":"de",
"Ghana":"gh",
"Iran":"ir",
"Japan":"jp",
"Korea Republic":"kr",
"Mexico":"mx",
"Morocco":"ma",
"Netherlands":"nl",
"Poland":"pl",
"Portugal":"pt",
"Qatar":"qa",
"Saudi Arabia":"sa",
"Senegal":"sn",
"Serbia":"rs",
"Spain":"es",
"Switzerland":"ch",
"Tunisia":"tn",
"USA":"us",
"Uruguay":"uy",
"Wales":"gb"
}

# -----------------------------
# criar gráfico
# -----------------------------

fig = go.Figure()

for _, row in team_stats.iterrows():

    team = row["team"]
    x = row["goals_scored"]
    y = row["goals_conceded"]

    if team in iso_map:

        flag_url = f"https://flagcdn.com/w40/{iso_map[team]}.png"

        fig.add_layout_image(
            dict(
                source=flag_url,
                xref="x",
                yref="y",
                x=x,
                y=y,
                sizex=0.15,
                sizey=0.15,
                xanchor="center",
                yanchor="middle"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker=dict(size=20, opacity=0),
                hovertemplate=
                f"<b>{team}</b><br>"
                f"Avg Goals Scored: {x:.2f}<br>"
                f"Avg Goals Conceded: {y:.2f}<extra></extra>"
            )
        )

# linhas médias

fig.add_vline(x=team_stats["goals_scored"].mean(), line_dash="dash")
fig.add_hline(y=team_stats["goals_conceded"].mean(), line_dash="dash")

# layout

fig.update_layout(
    title="World Cup 2022 — Attack vs Defense",
    xaxis_title="Average Goals Scored",
    yaxis_title="Average Goals Conceded",
    template="plotly_white"
)


fig.write_html("world_cup_attack_defense.html")