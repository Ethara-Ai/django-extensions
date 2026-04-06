import configparser


def parse_mysql_cnf(dbinfo):
    """
    Attempt to parse mysql database config file for connection settings.
    Ideally we would hook into django's code to do this, but read_default_file is
    handled by the mysql C libs so we have to emulate the behaviour

    Settings that are missing will return ''
    returns (user, password, database_name, database_host, database_port)
    """
    pass
