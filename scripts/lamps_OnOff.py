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

uniSet1 = [
#141,163,
#354,143,816,339,821,15,
#342,157,125,359,837,30,
#148,165,
#357,144,830,343,852,24,
#128,130,802,129,841,37,
#151,167,
#127,344,847,132,806,28,
146,346,803,355,818,45,
#155,168,
149,153,807,124,838,32,
164,131,39,666,834,22,
#161,171,
360,353,981,145,849,17,
335,350,980,348,805,4]


change(lamps, False)
