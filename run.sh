# /etc/init.d/rethinkdb start # only if not working
git pull
python engine.py &
python engine_worker.py &
python serial_worker.py &



