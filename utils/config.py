import json

config = json.load(open("./config.json", 'r', encoding="utf-8"))
g_poses = config["model"]["poses"]
g_probability_map = config["model"]["probability-map"]
for i in range(len(g_probability_map)):
    for j in range(1, len(g_probability_map[i])):
        g_probability_map[i][j] = g_probability_map[i][j - 1] + g_probability_map[i][j]
# print(g_probability_map)
