# /etc/init.d/rethinkdb start # only if not working
python engine.py &
python lamp_worker.py &


