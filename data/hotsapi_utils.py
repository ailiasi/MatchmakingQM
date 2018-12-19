#import json
import requests
import pandas as pd
from time import sleep

supports = ["Alexstrasza", "Ana", "Auriel", "Brightwing", "Deckard", "Kharazim", "Li Li", "Lt. Morales", 
            "Lúcio", "Malfurion", "Rehgar", "Stukov", "Tyrande", "Uther", "Whitemane"]
tanks = ["Anub'arak", 'Arthas', 'Blaze', 'Cho', 'Diablo', 'E.T.C.', 'Garrosh', 'Johanna',
         "Mal'Ganis", 'Muradin', 'Stitches', 'Tyrael',]
ranged_dps = ["Azmodan", "Cassia", "Chromie", "Falstad", "Fenix", "Cho'gall", "Genji", "Greymane",
              "Gul'dan", "Hanzo", "Jaina", "Junkrat", "Kael'thas", "Kel'Thuzad", "Li-Ming", "Lunara",
              "Mephisto", "Nazeebo", "Nova", "Orphea", "Probius", "Raynor", "Sgt. Hammer", "Sylvanas",
              "Tracer", "Tychus", "Valla", "Zagara", "Zul'jin"]

def gather_info(replay, fields = ["id", "game_type", "game_date", "game_length", "region"], with_players = True):
    dic = {key: replay[key] for key in fields}
    
    if with_players:
        ind_0 = 0
        ind_1 = 5
        for player in replay["players"]:
            if player["team"] == 0:
                dic["p" + str(ind_0)] = player["blizz_id"]
                dic["h" + str(ind_0)] = player["hero"]
                ind_0 += 1
            else:
                dic["p" + str(ind_1)] = player["blizz_id"]
                dic["h" + str(ind_1)] = player["hero"]
                ind_1 += 1
    return dic

def request_hotsAPI(params):       
    response = requests.get("https://hotsapi.net/api/v1/replays/", params = params)
    if response.status_code == 429:
        print(response.status_code)
        print("waiting 60 seconds")
        sleep(60)
        response = requests.get("https://hotsapi.net/api/v1/replays", params = params)

    if response.status_code != 200:
        data = None
    else:
        data = response.json()
    return (response.status_code, data)

def get_replay_data(start_date, end_date, min_id = "10000000",):
    params = {"min_id": min_id, 
              "start_date": start_date, 
              "end_date": end_date,
              "game_type":"QuickMatch",
              "with_players": True}
    lst = []
    
    print("Getting replays")
    for i in range(100):
        print(i,)
        (status, replays) = request_hotsAPI(params)
        if status != 200:
            print(i, status)
            break
        elif replays == []:
            print("Empty replay list, loop {}".format(i))
            break
        else:
            get_fields = lambda replay: gather_info(replay, 
                            fields = ["id", "game_date", "game_length", "region"], 
                            with_players = True)
            lst += [get_fields(replay) for replay in replays]
                
            params["min_id"] = str(int(replays[-1]["id"]) + 1)
    print("Found {} replays in the period between {} {}".format(len(lst), start_date, end_date))
    return pd.DataFrame(lst)

