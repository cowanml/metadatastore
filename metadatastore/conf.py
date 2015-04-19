import os
import yaml
import logging

logger = logging.getLogger(__name__)


def load_configuration(name, prefix, fields=None):
    """
    Load configuration data form a cascading series of locations.

    The precedence order is (highest priority last):

    1. CONDA_ENV/etc/{name}.yaml (if CONDA_ETC_ env is defined)
    2. /etc/{name}.yml
    3. ~/.config/{name}/connection.yml
    4. reading {PREFIX}_{FIELD} environmental variables

    Parameters
    ----------
    name : str
        The expected base-name of the configuration files

    prefix : str
        The prefix when looking for environmental variables

    fields : iterable of strings, optional
        Any required configuration fields.
        (in addition to ['database', 'host', 'port', 'alias'])

    Returns
    ------
    (db_connect_args:  [db, host, port, alias]
     timezone:  eg. 'US/Eastern'
     other:  dict of remaining fields, keyed on ``fields``,
             with the values extracted
     )
    """

    db_connect_args = set(['database', 'host', 'port', 'alias'])

    if fields is None:
        fields = db_connect_args
    else:
        fields = db_connect_args.union(set(fields))
        

    filenames = [os.path.join('/etc', name + '.yml'),
                 os.path.join(os.path.expanduser('~'), '.config',
                              name, 'connection.yml'),
                ]
    if 'CONDA_ETC_' in os.environ:
        filenames.insert(0, os.path.join(os.environ['CONDA_ETC_'],
                                         name + '.yml'))

    config = {}
    for filename in filenames:
        if os.path.isfile(filename):
            with open(filename) as f:
                config.update(yaml.load(f))
            logger.debug("Using db connection specified in config file. \n%r",
                         config)

    for field in fields.union(set(config.keys())):
        var_name = (prefix + '_' + field.upper()).replace(' ', '_')
        config[field] = os.environ.get(var_name, config.get(field, None))

    missing = [k for k, v in config.items() if v is None and k in fields]
    if missing:
        raise KeyError("The required configuration field(s), {0}"
                       ", were not found in any file or"
                       " environment variable.".format(missing))

    alias = config['alias']  # don't pop!  need in db_params too!
    timezone = config.pop('timezone')

    db_params = {}
    for key in db_connect_args:
        db_params[key] = config.pop(key)
    
    return (db_params, alias, timezone, config)


(db_connect_args, ALIAS, timezone, other
        ) = load_configuration('metadatastore', 'MDS')
