# /etc/init.d/rethinkdb start # only if not working
git pull
python engine.py &
python lamp_worker.py &


