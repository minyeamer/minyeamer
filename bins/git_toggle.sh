#!/bin/bash

echo "old email"
old=`git config user.email`
echo $old

if [ $old == "minyeamer@gmail.com" ]
then
  new="kimmy9809@gmail.com"
else
  new="minyeamer@gmail.com"
fi

git config --global user.email $new
# git config --global user.name minyeamer

echo "new email"
git config user.email
