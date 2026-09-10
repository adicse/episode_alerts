

swallowed_star_regex='Swall.*?Episode.*?(?=<)'
swallowed_star_link='https://animexin.dev/swallowed-star-season-5' 

export SED_DELIM=$'\03'

function get_axing_latest_episode() {
    local series_name="$1"
    local url="$2"
    local episode_regex="$3"
    local page="$(curl -ksL "${url}")"

    local latest_episode="$(echo "${page}" | grep -m 1 -P -o ${episode_regex})"

    grep "${latest_episode}" latest_episodes.txt
    if [[ "$?" -eq 0 ]]; then
        # no new episode
        return
    fi

    sed -i "s${SED_DELIM}${series_name}:.*${SED_DELIM}${series_name}: ${latest_episode}${SED_DELIM}" latest_episodes.txt

}


get_axing_latest_episode $swallowed_star_link $swallowed_star_regex