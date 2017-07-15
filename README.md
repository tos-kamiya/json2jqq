json2jqq
========

Suppose you got a json data, which you do not know structure, but have to analyze... `json2qq` is here.

A CLI Tool to extract query templates for [jq](https://stedolan.github.io/jq/) tool from json data.

## Installation

Install: 

```sh
sudo pip3 install git+https://github.com/tos-kamiya/json2jqq.git
```

Uninstall:

```sh
sudo pip3 uninstall json2jqq
```

## Tutorial

Extract a query template for `jq` from json data.

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
```

Each of extracted queries will work as `jq`'s filter.

```sh
$ jq '.[].url' myrepos.json
"https://github.com/tos-kamiya/json2jqq/"
"https://github.com/tos-kamiya/giftplayer/"
```
