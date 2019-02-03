cd /root/gowl
git clean -f; git stash; git fetch origin master; git pull --rebase origin master;
bash run.sh $1