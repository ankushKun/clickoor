#!/usr/bin/bash

me=$(whoami)
cd /home/$me/clickoor

# Check for internet connection using ping
if ping -c 1 google.com &> /dev/null; then
    # online
    repo="ankushKun/clickoor"

    cver=$(cat current)
    echo "current version: $cver"

    ver=$(curl -s https://api.github.com/repos/$repo/releases/latest | grep tag_name | cut -d : -f 2 | tr -d , | tr -d \"  | cut -d , -f 1 | awk '{$1=$1};1')

    echo "latest version: $ver"

    if [ "$ver" != "$cver" ]; then
        echo "updating..."
        zip_url=$(curl -s https://api.github.com/repos/$repo/releases/latest | grep zipball_url | cut -d : -f 2,3 | tr -d , | tr -d \"  | cut -d , -f 1 | awk '{$1=$1};1')
        echo "downloading $zip_url"
        curl -L -o update.zip $zip_url
        unzip update.zip -d update
        unzip_folder=$(ls update)
        rsync -av update/$unzip_folder/ ./
        rm update.zip
        rm -rf update
        echo $ver > current
    else
        echo "already up to date"
    fi
else
    # offline
    echo "offline, skipping update check"
fi
