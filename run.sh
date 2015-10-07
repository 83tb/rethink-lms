# /etc/init.d/rethinkdb start # only if not working
python engine.py &
python serial_worker.py &
python engine_worker.py &
python button_worker.py &



