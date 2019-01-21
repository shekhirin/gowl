cd /root/goalboard
git stash; git fetch origin master; git pull --rebase origin master;
python manage.py runserver
