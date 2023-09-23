from jsthon import JsthonDb

db = JsthonDb('reservations.json')

db.create_table('user')
db.add_new_keys(['id', 'username', 'password', 'created_at', 'updated_at'])


db.create_table('booking')
db.add_new_keys(['id', 'user_id', 'start_time', 'end_time', 'comment'])
