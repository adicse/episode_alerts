import requests
import re


def get_axing_latest_episode(series_link: str, episodes_to_find: dict):
    resp = requests.get(series_link)
    series_page = resp.text
    
    episode_names = []
    for episode in ["nextepisode", "previousepisode"]:
        episode_names.append(
            f"(?<=>){re.sub(r'\s+', ' ', episodes_to_find[episode]["name"]).replace(' ', '.*?')}[^<>]+"
            )
        
    regexp = re.compile('|'.join(episode_names), re.IGNORECASE)
    
    released_episode = re.findall(regexp, series_page)
    return released_episode
        
        
    

def tvmz_get_curr_and_next_episode(series_id: int) -> dict[str, str]:
    episode_details = {}
    api = f"https://api.tvmaze.com/shows/{series_id!s}?embed=nextepisode"
    resp = requests.get(api)
    
    resp.raise_for_status()
    
    
    return resp.json()['_links']

def main():
    latest_episode = tvmz_get_curr_and_next_episode(52178)
    available_on_animexin = get_axing_latest_episode('https://animexin.dev/swallowed-star-season-5/', latest_episode)
    print(available_on_animexin)

if __name__ == '__main__':
    main()