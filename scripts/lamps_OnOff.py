import rethinkdb as r

conn = r.connect("localhost").repl()
db = r.db("engine")
lamps_table = db.table("lamps")

ON_VALUE = 255
OFF_VALUE = 0


def change(lamp_numbers, state):
    for lamp_number in lamp_numbers:
        special_l_setting = OFF_VALUE
        if state:
            special_l_setting = ON_VALUE

        new = dict(
            special_l_setting=special_l_setting,
            change_required=True
        )

        print str(lamps_table.filter({'hardware': {'address': str(lamp_number)}}).update(new))
        a = lamps_table.filter(
            {'hardware': {'address': str(lamp_number)}}).update(new).run(conn)
        print "Received from rethinkdb: %s", str(a)


# lampsOff = [
#     682, 700, 959, 100, 696, 687, 364, 432,
#     789, 556, 707, 421, 972, 693,
#     770, 77, 319, 603,	711, 878, 391, 93,
#     54, 876, 880, 94, 105, 297
# ]
lamps = [
    126, 862, 984, 843,
    682, 700, 959, 100, 696, 687, 364, 432,
    789, 556, 707, 421, 972, 693,
    770, 77, 319, 603,	711, 878, 391, 93,
    54, 876, 880, 94, 105, 297
]

change(lamps, False)
