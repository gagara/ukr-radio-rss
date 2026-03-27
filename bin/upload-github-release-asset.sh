#!/usr/bin/env bash

USAGE="$0 -o <owner> -r <repo> -t <tag> -f <file>"

[[ -z "${GH_TOKEN}" ]] && echo "Error: GH_TOKEN environment not set" && exit 1

while getopts "o:r:t:f:" opt; do
    case $opt in
        o)
            OWNER=$OPTARG ;;
        r)
            REPO=$OPTARG ;;
        t)
            TAG=$OPTARG ;;
        f)
            FILE=$OPTARG ;;
    esac
done

[[ -z "${OWNER}" ]] || [[ -z "${REPO}" ]] || [[ -z "${TAG}" ]] || [[ -z "${FILE}" ]] && echo "$USAGE" && exit 1

GH_API="https://api.github.com"
GH_REPO="${GH_API}/repos/${OWNER}/${REPO}"
GH_TAGS="${GH_REPO}/releases/tags/${TAG}"
AUTH="Authorization: token ${GH_TOKEN}"

# get release info
response=$(curl -sH "$AUTH" $GH_TAGS)
upload_url=$(echo $response | jq '.upload_url' | sed -E 's/\{.*\}//' | tr -d '"')
upload_url="${upload_url}?name=$(basename $FILE)"

# delete asset first
for row in $(echo $response | jq '.assets | map({name: .name, url: .url})' | jq -c '.[]'); do
  name=$(echo ${row} | jq -r '.name')
  if [ "$name" == "$(basename $FILE)" ]; then
    delete_url=$(echo ${row} | jq -r '.url')
    echo -n "Deleting asset ${name}..."
    rsp=$(curl -sH "$AUTH" -o /dev/null -w "%{http_code}" -X "DELETE" "${delete_url}")
    echo "[$rsp]"
    break
  fi
done

# upload asset
echo -n "Uploading asset ${FILE}..."
rsp=$(curl -sH "$AUTH" -H "Content-Type: application/octet-stream" -o /dev/null -w "%{http_code}" --data-binary @$FILE "$upload_url")
echo "[$rsp]"
