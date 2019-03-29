import pandas as pd
import private
import psycopg2
import requests
import settings


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

def write_data_to_database(conn, row):

    try:
        cur = conn.cursor()
        cur.execute(settings.QUERY_INSERT, row)
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


if __name__ == '__main__':
    keyword = 'chipotle'
    zipcodes_latitudes_longitudes = get_list_of_dictionaries_from_database(settings.QUERY_SEARCH_DATA)

    import ipdb; ipdb.set_trace()
    for api_inputs in zipcodes_latitudes_longitudes:
        zip_code = api_inputs.pop('zip')
        api_inputs.update({'keyword': keyword})
        print(api_inputs)
        data = get_google_map_api_data(**api_inputs)

        if data['results']:

            for d in data['results']:
                row = parse_google_maps_data(d)
                row.update(api_inputs)
                row.update({'zip_code': zip_code})

                with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:
                    write_data_to_database(conn, row)
