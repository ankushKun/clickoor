#!/usr/bin/bash

me=$(whoami)
cd /home/$me/infinitycam

# Check for internet connection
echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    # online
    repo="ankushKun/infinitycam"

    cver=$(cat current)
    echo "current version: $cver"

    ver=$(curl -s https://api.github.com/repos/$repo/releases/latest | grep tag_name | cut -d : -f 2 | tr -d , | tr -d \"  | cut -d , -f 1 | awk '{$1=$1};1')

    echo "latest version: $ver"

    if [ "$ver" != "$cver" ]; then
        echo "updating..."
        zip_url=$(curl -s https://api.github.com/repos/$repo/releases/latest | grep zipball_url | cut -d : -f 2,3 | tr -d , | tr -d \"  | cut -d , -f 1 | awk '{$1=$1};1')
        echo "downloading $zip_url"
        curl -L -o update.zip $zip_url
        unzip -o -j update.zip -d ./update
        mv update/*/* .
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




