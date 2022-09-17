#!/bin/bash

username=$1
repository=$2

# git init
# touch README.md
# git add README.md
git commit -m "feat: git init"
git branch -M main
git remote add origin https://github.com/$username/$repository.git
git set-url origin https://$username@github.com/$username/$repository.git
git push -u origin main
