json2jqq
========

CLI Tool to extract query templates for [jq](https://stedolan.github.io/jq/) tool from json data.

## Installation

```sh
cd /directory/where/json2jqq/was/downloaded
sudo pip3 install .
```

## Tutorial

```sh
$ bash
$ cat > myrepos.json <<EOF
[
  { "author": "Toshihiro Kamiya", "url": "https://github.com/tos-kamiya/json2jqq/" },
  { "author": "Toshihiro Kamiya", "url": "https://github.com/tos-kamiya/giftplayer/" }
]
EOF
$ cat myrepos.json | json2jqq
.[].author
.[].url
$ jq '.[].url' myrepos.json
"https://github.com/tos-kamiya/json2jqq/"
"https://github.com/tos-kamiya/giftplayer/"
```
