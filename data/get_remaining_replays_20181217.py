import hotsapi_utils

for dates, min_id in [(("2018-11-19","2018-11-26"), "13682188")]:#"13401488"),(("2018-12-03","2018-12-10"), "13669457")]:
    replays = hotsapi_utils.get_replay_data(*dates, min_id = min_id)
    replays.to_csv("original/matches-{}--{}.csv".format(*dates), mode = "a", header = False, encoding = "utf-8")