import hotsapi_utils

for dates in [("2018-11-19","2018-11-26"),("2018-12-03","2018-12-10")]:
    replays = hotsapi_utils.get_replay_data(*dates)
    replays.to_csv("original/matches-{}--{}.csv".format(*dates), encoding = "utf-8")
