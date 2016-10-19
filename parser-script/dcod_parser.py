#!/usr/bin/python3
import sys
import argparse
import MySQLdb
import json


def main(args):

    data = []
    try:
        f = open(args.datafile, 'r')
    except IOError:
        print('Cannot open', args.datafile)
        sys.exit(0)
    else:
        data = json.loads(f.read())
        f.close()

    data = unify_data(data)

    update_database(data, args)

    print ("Database is up to date now.")


def unify_data(data):
    ''' Get rid of the repeated use of the region name
        and reorganize data in more convenient structure '''

    unified_data = {}

    for el in data['data']:
        region = el['Регион']
        country_value = (el['Страна'], el['Значение'])

        if region in unified_data:
            unified_data[region].append(country_value)
        else:
            unified_data[region] = [country_value]

    return unified_data


def update_database(data, args):
    db = MySQLdb.connect(host = args.db_host, db = args.db_name, user = args.db_user,
                         passwd = args.db_pass, charset = 'utf8')

    regions_ids = update_regions(db, data.keys())
    update_countries_values(db, data, regions_ids)

    db.close()


def update_regions(db, regions_keys):
    ''' Checks if the regions are in the database. Inserts the missing regions.
        Returns "region => id" dictionary. '''

    regions = list(regions_keys)
    regions_ids = {}

    cursor = db.cursor()
    sql_select = '''SELECT region_id FROM dcodgraph_regions WHERE name = %s;'''

    for region in sorted(regions):

        cursor.execute(sql_select,(region,))
        region_id = cursor.fetchone()

        if region_id:
            region_id = region_id[0]
        else:
            sql = '''INSERT INTO dcodgraph_regions (name) VALUES (%s);'''
            run_db_statement(db, cursor, sql, (region,))
            region_id = cursor.lastrowid

        regions_ids[region] = region_id
    cursor.close()

    return regions_ids


def update_countries_values(db, data, regions_ids):
    ''' Checks if all countries with appropriate values are in the database.
        Inserts the missing countries with their values.
        Update countries' values if a value is out of date.'''

    cursor = db.cursor()

    for region, counties_values in data.items():
        region_id = regions_ids[region]
        sql_select = '''SELECT value FROM dcodgraph_countriesvalues
                        WHERE country = %s AND region_id = %s;'''

        for country, new_value in counties_values:

            cursor.execute(sql_select,(country,region_id))
            db_value = cursor.fetchone()

            if not db_value:

                sql = '''INSERT INTO dcodgraph_countriesvalues
                                (region_id, country, value) VALUES (%s, %s, %s);'''
                run_db_statement(db, cursor, sql, (region_id, country, new_value))

            elif float(db_value[0]) != float(new_value):

                sql = '''UPDATE dcodgraph_countriesvalues SET value = %s
                                WHERE country = %s AND region_id = %s;'''
                run_db_statement(db, cursor, sql, (new_value, country, region_id))

    cursor.close()


def run_db_statement(db, cursor, sql, args):
    try:
        cursor.execute(sql,args)
        db.commit()
    except:
        db.rollback()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='''Dcod data parser. It parses specified JSON file and puts the data into the database''')

    parser.add_argument('datafile', metavar='JSON_FILE_PATH', help='path to a JSON file with data')
    parser.add_argument('--db_host', default='localhost', help='database host (default: localhost)')
    parser.add_argument('--db_name', default='dcod', help='database name (default: dcod)')
    parser.add_argument('--db_user', default='dcod_user', help='database user (default: dcod_user)')
    parser.add_argument('--db_pass', default='dcod123', help='database password (default: dcod123)')

    args = parser.parse_args()


    main(args)
