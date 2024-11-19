#!/bin/bash

# Inspired by https://github.com/4ms/4ms-kicad-lib/blob/master/PCM/make_archive.sh

echo "Version (e.g. 1.0.1): "
read version

cd ./PartyWagon112-KiCad-Library

echo "Zipping archive: "
rm -f PartyWagon112-KiCad-Library-$version.zip
zip -r PartyWagon112-KiCad-Library-$version.zip footprints/ symbols/ resources/ metadata.json -x "*.DS_Store" -x "*/\.*"

# echo "Copying metadata.json and icon.png"
# cp metadata.json PCM/metadata.json
# cp resources/icon.png PCM/icon.png

download_sha256=$(shasum --algorithm 256 PCM/PartyWagon112-KiCad-Library-$version.zip | xargs | cut -d' ' -f1)
download_size=$(ls -l PartyWagon112-KiCad-Library-$version.zip | xargs | cut -d' ' -f5)
install_size=$(unzip -l PartyWagon112-KiCad-Library-$version.zip | tail -1 | xargs | cut -d' ' -f1)

echo "Edit these json values in PCM/metadata.json:"
echo "\"download_sha256\": \"$download_sha256\","
echo "\"download_size\": $download_size,"
echo "\"download_url\": \"https://github.com/partywagon112/PartyWagon112-KiCad-Library/releases/download/$version/PartyWagon112-KiCad-Library-$version.zip\","
echo "\"install_size\": $install_size,"