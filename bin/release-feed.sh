#!/bin/bash

GH_OWNER="gagara"
GH_REPO="ukr-radio-rss"
GH_TAG="latest"

USAGE="$0 -s <spider>"

while getopts "s:" opt; do
    case $opt in
        s)
            SPIDER=$OPTARG ;;
    esac
done

[[ -z "${SPIDER}" ]] && echo "$USAGE" && exit 1

FEED_FILE="${SPIDER}-feed.rss"

rm -f ${FEED_FILE}

scrapy crawl ${SPIDER}

if [ -f "${FEED_FILE}" ]; then
    $(dirname $0)/upload-github-release-asset.sh -o ${GH_OWNER} -r ${GH_REPO} -t ${GH_TAG} -f ${FEED_FILE}
fi
