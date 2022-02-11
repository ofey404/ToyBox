#!/usr/bin/env bash

# nhentai.net may limit the maximum link number to about 20, manually tested.

# set -x             # for debug
set -euo pipefail  # fail early
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" 

proxychains curl https://i.nhentai.net/galleries/2081195/0.jpg > ${SCRIPT_DIR}/data/0.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/1.jpg > ${SCRIPT_DIR}/data/1.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/2.jpg > ${SCRIPT_DIR}/data/2.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/3.jpg > ${SCRIPT_DIR}/data/3.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/4.jpg > ${SCRIPT_DIR}/data/4.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/5.jpg > ${SCRIPT_DIR}/data/5.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/6.jpg > ${SCRIPT_DIR}/data/6.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/7.jpg > ${SCRIPT_DIR}/data/7.jpg &
proxychains curl https://i.nhentai.net/galleries/2081195/8.jpg > ${SCRIPT_DIR}/data/8.jpg
proxychains curl https://i.nhentai.net/galleries/2081195/9.jpg > ${SCRIPT_DIR}/data/9.jpg

for i in {1..18}; do
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}0.jpg > ${SCRIPT_DIR}/data/${i}0.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}1.jpg > ${SCRIPT_DIR}/data/${i}1.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}2.jpg > ${SCRIPT_DIR}/data/${i}2.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}3.jpg > ${SCRIPT_DIR}/data/${i}3.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}4.jpg > ${SCRIPT_DIR}/data/${i}4.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}5.jpg > ${SCRIPT_DIR}/data/${i}5.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}6.jpg > ${SCRIPT_DIR}/data/${i}6.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}7.jpg > ${SCRIPT_DIR}/data/${i}7.jpg &
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}8.jpg > ${SCRIPT_DIR}/data/${i}8.jpg
    proxychains curl https://i.nhentai.net/galleries/2081195/${i}9.jpg > ${SCRIPT_DIR}/data/${i}9.jpg
done



