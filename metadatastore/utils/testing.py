import uuid
import os
from metadatastore.api import db_connect, db_disconnect
import os

conn = None

test_db_name = "mds_testing_disposable_{}".format(str(uuid.uuid4()))
test_db_host = 'localhost'
test_db_port = '27017'
test_db_alias = 'mds'


def db_setup(collections):
    "Create a fresh database with unique (random) name."
    global conn
    db_disconnect(collections)
    conn = db_connect(test_db_name, test_db_host,
                      int(test_db_port), test_db_alias)


def db_teardown(collections, drop_db=None):
    "Drop the fresh database and disconnect."

    if drop_db == True:
        conn.drop_database(test_db_name)
    db_disconnect(collections)
