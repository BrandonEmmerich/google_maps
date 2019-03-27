import private
import psycopg2
import requests
import settings

def get_raw_data():
    url = 'https://gist.githubusercontent.com/abatko/ee7b24db82a6f50cfce02afafa1dfd1e/raw/36d2c74bc3f2ea777449349cf290d490e0d62dc3/US%2520Zip%2520Code%2520Geolocations%2520from%25202018%2520Government%2520Data'
    response = requests.get(url)
    raw_data = response.text

    return raw_data

def parse_raw_data(line):
    objects = line.split(',')
    row = {
        'zip': objects[0],
        'latitude': float(objects[1]),
        'longitude': float(objects[2]),
        }
    return row

def write_data_to_database(conn, row):

    try:
        cur = conn.cursor()
        cur.execute(settings.QUERY_INSERT_ZIP_CODES, row)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print e

if __name__ == '__main__':
    raw_data = get_raw_data()
    lines = raw_data.split('\n')

    with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:
        for line in lines[1:]:
            row = parse_raw_data(line)
            print(row)
            write_data_to_database(conn, row)
