from data_processing import load_world_cup_2022, create_team_table, get_goal_scorers

#Carregando dados da copa

matches = load_world_cup_2022()
table = create_team_table(matches)
scorers = get_goal_scorers(matches)

#Salvando arquivos CSV

matches.to_csv("../data/wc_matches.csv", index=False)
table.to_csv("../data/wc_table.csv", index=False)
scorers.to_csv("../data/wc_scorers.csv", index=False)

#Arquivos salvos
