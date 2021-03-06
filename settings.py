QUERY_CREATE_TABLE = '''
CREATE TABLE locations_data.manhattan_{} (
    rating double precision,
    user_ratings_total double precision,
    result_name character varying,
    location_latitude double precision,
    location_longitude double precision,
    place_id character varying,
    vicinity character varying,
    id character varying,
    latitude double precision,
    longitude double precision,
    keyword character varying,
    zip_code character varying,
    date_added timestamp
);
'''

QUERY_INSERT = '''
    INSERT INTO locations_data.manhattan_{}
    (rating, user_ratings_total, result_name, location_latitude, location_longitude,
    place_id, vicinity, id, latitude, longitude, keyword, zip_code, date_added)
    VALUES
    (%(rating)s, %(user_ratings_total)s, %(result_name)s, %(location_latitude)s, %(location_longitude)s,
    %(place_id)s, %(vicinity)s, %(id)s, %(latitude)s, %(longitude)s, %(keyword)s, %(zip_code)s, %(date_added)s)
     '''

QUERY_INSERT_ZIP_CODES = '''
    INSERT INTO locations_data.us_zip_codes
    (zip, latitude, longitude)
    VALUES
    (%(zip)s, %(latitude)s, %(longitude)s)
'''

QUERY_SEARCH_DATA = '''
select
    zip,
    latitude,
    longitude
from locations_data.us_zip_codes
where zip in (
	'10026', '10027', '10030', '10037', '10039', '10001', '10011', '10018',
	'10019', '10020', '10036', '10029', '10035', '10010', '10016', '10017', '10022', '10012', '10013', '10014',
	'10004', '10005', '10006', '10007', '10038', '10280', '10002', '10003', '10009', '10021', '10028',
	'10044', '10065', '10075', '10128', '10023', '10024', '10025', '10031', '10032', '10033', '10034', '10040'
	);
'''
