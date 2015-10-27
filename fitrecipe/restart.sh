git pull

ps aux | grep 'uwsgi --socket :10001' | awk '{print $2}' | xargs kill -15;

sleep 3;

uwsgi --socket :10001 --processes 2 --chdir /home/work/fitRecipe/fitrecipe --module django_wsgi --logto /home/work/logs/uwsgi_log&
