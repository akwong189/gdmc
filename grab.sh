#!/bin/bash
mkdir server
curl https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar -o server.jar
unzip -q server.jar -d server
mv server/data/minecraft/structures/village villages
rm -rf server
rm server.jar