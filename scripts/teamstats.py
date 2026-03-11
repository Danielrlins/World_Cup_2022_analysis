import pandas as pd

df = pd.read_csv("wc_matches.csv")

home = pd.DataFrame({
    "Team": df["home_team"],
    "Goals Scored": df["home_score"],
    "Goals Conceded": df["away_score"]
})

away = pd.DataFrame({
    "Team": df["away_team"],
    "Goals Scored": df["away_score"],
    "Goals Conceded": df["home_score"]
})

teams = pd.concat([home, away])

team_stats = teams.groupby("Team").agg({
    "Goals Scored":"sum",
    "Goals Conceded":"sum",
    "Team":"count"
}).rename(columns={"Team":"Matches"}).reset_index()

team_stats["Avg Goals Scored"] = team_stats["Goals Scored"] / team_stats["Matches"]
team_stats["Avg Goals Conceded"] = team_stats["Goals Conceded"] / team_stats["Matches"]

print(team_stats)

team_stats.to_csv("wc_team_stats.csv", index=False)
