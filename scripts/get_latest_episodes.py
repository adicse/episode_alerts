import requests
import json


DATA_FILE = 'data/latest_episodes.json'

def tvmz_get_curr_and_next_episode(series_id: int) -> dict[str, str]:
    api = f"https://api.tvmaze.com/shows/{series_id!s}?embed=nextepisode"
    resp = requests.get(api)
    
    resp.raise_for_status()
    temp_dict = resp.json()['_links']
    print(temp_dict)
    temp_dict['name'] = resp.json()['name']
    if 'self' in temp_dict:
        del temp_dict['self']
        
    return temp_dict

def get_latest_episode(series_name: str):
    series_episodes = tvmz_get_curr_and_next_episode(52178)
    latest_episodes = {}
    
    
    with open(DATA_FILE) as fr:
        latest_episodes = json.load(fr)
        
    series = latest_episodes.get(series_name, {})
    series['aired_episode'] = series_episodes['previousepisode']
    
    latest_episodes[series_name] = series
    
    with open(DATA_FILE, 'w') as fw:
        json.dump(latest_episodes, fw)    

if __name__ == '__main__':
    get_latest_episode('swallowed_star')