import requests
import json


DATA_FILE = 'data/latest_episodes.json'

def tvmz_get_curr_and_next_episode(series_id: int) -> dict[str, str]:
    api = f"https://api.tvmaze.com/shows/{series_id!s}?embed=nextepisode"
    resp = requests.get(api)
    
    resp.raise_for_status()
    temp_dict = resp.json()['_links']
    temp_dict['name'] = resp.json()['name']
    if 'self' in temp_dict:
        del temp_dict['self']
        
    return temp_dict

def get_latest_episode(series_name: str):
    latest_episodes = {}
    
    with open(DATA_FILE) as fr:
        latest_episodes = json.load(fr)
        
    series_episodes = tvmz_get_curr_and_next_episode(latest_episodes[series_name]['tvmaze_id'])
    print(series_episodes)
        
    series = latest_episodes.get(series_name, {})
    series['aired_episode'] = series_episodes['previousepisode']
    print(f"aired_episode: {series['aired_episode']}")

    latest_episodes[series_name] = series
    
    with open(DATA_FILE, 'w') as fw:
        json.dump(latest_episodes, fw)    

if __name__ == '__main__':
    get_latest_episode('swallowed_star')