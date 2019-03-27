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

def get_coordinates(zip):
    with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:

        cur = conn.cursor()
        cur.execute(settings.QUERY_LAT_LONG.format(str(zip)))
        data = cur.fetchone()

        row = {
            'latitude': data[1],
            'longitude': data[2],
        }

    return row


if __name__ == '__main__':

    api_inputs = []
    for keyword in settings.search_terms:
        for zip in settings.manhattan_zip_codes:
            search_data = get_coordinates(zip)
            search_data.update({'keyword': keyword})
            api_inputs.append(search_data)


    for search_data in api_inputs:
        print(search_data)

        data = get_google_map_api_data(**search_data)

        if data['results']:

            for d in data['results']:
                row = parse_google_maps_data(d)
                row.update(search_data)

                with psycopg2.connect(private.AWS_CONNECTION_STRING) as conn:
                    write_data_to_database(conn, row)
