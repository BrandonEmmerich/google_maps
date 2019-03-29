import datetime
import pandas as pd
import private
import psycopg2
import requests
import settings
import sys

def get_google_map_api_data(latitude, longitude, keyword):
    url_base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1000&keyword={keyword}&key={api_key}'
    url = url_base.format(api_key = private.API_KEY, latitude = latitude, longitude = longitude, keyword=keyword)
    _json = requests.get(url)
    data = _json.json()

    return data

def parse_google_maps_data(_dict):

    row = {
        'rating': _dict.get('rating'),
        'user_ratings_total': _dict.get('user_ratings_total'),
        'result_name': _dict.get('name'),
        'location_latitude': _dict['geometry']['location'].get('lat'),
        'location_longitude': _dict['geometry']['location'].get('lng'),
        'place_id': _dict.get('place_id'),
        'vicinity': _dict.get('vicinity'),
        'id': _dict.get('id'),
    }

    return row

def write_data_to_database(row, query):
    with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, row)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)

def get_list_of_dictionaries_from_database(query):
    with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:
        df = pd.read_sql(
            sql = query,
            con = conn
        )
        list_of_dictionaries = df.to_dict('records')

        return list_of_dictionaries

def execute_query(query):
    with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:
        cur = conn.cursor()
        cur.execute(query)


if __name__ == '__main__':
    keyword = str(sys.argv[1])
    keyword_clean = keyword.replace(" ", "_")
    date_added = datetime.datetime.now()

    query_create_table = settings.QUERY_CREATE_TABLE.format(keyword_clean)
    query_insert_row = settings.QUERY_INSERT.format(keyword_clean)

    execute_query(query_create_table)
    zipcodes_latitudes_longitudes = get_list_of_dictionaries_from_database(settings.QUERY_SEARCH_DATA)

    for api_inputs in zipcodes_latitudes_longitudes:
        zip_code = api_inputs.pop('zip')
        api_inputs.update({'keyword': keyword})
        print('Keyword: ' + keyword + ', Zip: ' + zip_code)
        data = get_google_map_api_data(**api_inputs)

        if data['results']:

            for d in data['results']:
                row = parse_google_maps_data(d)
                row.update(api_inputs)
                row.update({
                    'zip_code': zip_code,
                    'date_added': date_added,
                    })

                write_data_to_database(row, query_insert_row)
