git filter-branch --env-filter '
OLD_EMAIL="old@gmail.com"
NOW_NAME="name"
NOW_EMAIL="now@gmail.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ] 
then
    export GIT_COMMITTER_NAME="$NOW_NAME" 
    export GIT_COMMITTER_EMAIL="$NOW_EMAIL" 
fi 
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ] 
then 
    export GIT_AUTHOR_NAME="$NOW_NAME"
    export GIT_AUTHOR_EMAIL="$NOW_EMAIL" 
fi 
' --tag-name-filter cat -- --branches --tags
# git push --force --tags origin 'refs/heads/[branch]'
