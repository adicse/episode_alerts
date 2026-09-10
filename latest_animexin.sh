

swallowed_star_regex='Swall.*?Episode.*?(?=<)'
swallowed_star_link='https://animexin.dev/swallowed-star-season-5' 

function get_axing_latest_episode() {
    local url="$1"
    local episode_regex="$2"
    local page="$(curl -ksL "${url}")"

    echo "${page}" | grep -m 1 -P -o ${episode_regex}
}


get_axing_latest_episode $swallowed_star_link $swallowed_star_regex