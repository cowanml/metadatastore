import uuid
from metadatastore.api import db_connect, db_disconnect

conn = None

test_db_params = {'database': "mds_testing_disposable_{0}".format(str(uuid.uuid4())),
                  'host': 'localhost',
                  'port': 27017,
                  'alias': 'mds'}


def dbtest_setup(collections, test_db_params):
    "Create a fresh database with unique (random) name."
    global conn
    db_disconnect(collections)
    conn = db_connect(**test_db_params)


def dbtest_teardown(collections, test_db_params, drop_db=True):
    "Drop the fresh database and disconnect."

    if drop_db != False:
        conn.drop_database(test_db_params['database'])
    db_disconnect(collections)
