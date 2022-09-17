#!/bin/bash

echo "[old info]"
old_name=`git config user.name`
echo $old_name
git config user.email

if [ $old_name == "minyeamer" ]
then
  new_name="minywork"
  new_email="kimmy9809@gmail.com"
else
  new_name="minyeamer"
  new_email="minyeamer@gmail.com"
fi

git config --global user.name $new_name
git config --global user.email $new_email

echo "[new info]"
git config user.name
git config user.email
