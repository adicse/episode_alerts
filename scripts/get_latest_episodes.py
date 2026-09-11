import json

import requests

DATA_FILE = "data/latest_episodes.json"


def tvmz_get_curr_and_next_episode(series_id: int) -> dict[str, str]:
    api = f"https://api.tvmaze.com/shows/{series_id!s}?embed=nextepisode"
    resp = requests.get(api)

    resp.raise_for_status()
    temp_json = resp.json()

    return_dict = resp.json()["_links"]
    return_dict["name"] = temp_json["name"]
    return_dict["id"] = temp_json["id"]

    temp_json = resp.json()["_embedded"]["nextepisode"]
    return_dict["season"] = temp_json["season"]
    return_dict["number"] = temp_json["number"] - 1

    if "self" in return_dict:
        del return_dict["self"]

    return return_dict


def get_latest_episode(series_name: str):
    latest_episodes = {}

    with open(DATA_FILE) as fr:
        latest_episodes = json.load(fr)

    if not latest_episodes.get(series_name):
        print("series details not in json file")
        print(latest_episodes)
    elif not latest_episodes.get(series_name).get("tvmaze_id"):
        print(f"tvmaze id not in json file for : {series_name}")
        print(latest_episodes[series_name])

    series_episodes = tvmz_get_curr_and_next_episode(
        latest_episodes[series_name]["tvmaze_id"]
    )
    print(series_episodes)

    series = latest_episodes.get(series_name, {})
    series["aired_episode"] = {}
    for key in ["name", "season", "number"]:
        series["aired_episode"][key] = series_episodes[key]

    series["tvmaze_id"] = series_episodes["id"]

    print(f"aired_episode: {series['aired_episode']}")

    latest_episodes[series_name] = series

    with open(DATA_FILE, "w") as fw:
        json.dump(latest_episodes, fw)


if __name__ == "__main__":
    get_latest_episode("swallowed_star")
