#!/bin/bash

swallowed_star_regex='Swall.*?Episode.*?(?=<)'
swallowed_star_link='https://animexin.dev/swallowed-star-season-5' 

GIT_ROOT="$(command git rev-parse --show-toplevel 2> /dev/null)"

export SED_DELIM=$'\03'

function get_axing_latest_episode() {
    local series_name="$1"
    local url="$2"
    local episode_regex="$3"
    local temp_page="/tmp/page.txt"
    local data_file="${GIT_ROOT}/data/latest_episodes.txt"

    qInfo "getting page: ${url}"
    curl -sL \
        -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0.0.0 Safari/537.36' \
        "${url}" -o "${temp_page}"

    local latest_episode="$(cat "${temp_page}" | grep -m 1 -P -o ${episode_regex})"
    if [[ -z "${latest_episode// /}" ]]; then
        echo "Could not find latest episode"
        exit 1
    fi

    grep "${latest_episode}" "${data_file}"
    if [[ "$?" -eq 0 ]]; then
        # no new episode
        fnInfo "No new episode released"
        return
    else
        green "New episode released"
    fi

    if grep -qF "${series_name}:" "${data_file}"; then
        sed -i "s${SED_DELIM}^${series_name}:.*${SED_DELIM}${series_name}: ${latest_episode}${SED_DELIM}" \
            "${data_file}"
    else
        printf '%s: %s\n' "$series_name" "$latest_episode" >> "${data_file}"
    fi

}


get_axing_latest_episode "Swallowed_star" $swallowed_star_link $swallowed_star_regex