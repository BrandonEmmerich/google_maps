QUERY_INSERT = '''
    INSERT INTO locations_data.manhattan_coffee
    (rating, user_ratings_total, result_name, location_latitude, location_longitude,
    place_id, vicinity, id, latitude, longitude, keyword, zip_code)
    VALUES
    (%(rating)s, %(user_ratings_total)s, %(result_name)s, %(location_latitude)s, %(location_longitude)s,
    %(place_id)s, %(vicinity)s, %(id)s, %(latitude)s, %(longitude)s, %(keyword)s, zip_code)
     '''

QUERY_INSERT_ZIP_CODES = '''
    INSERT INTO locations_data.us_zip_codes
    (zip, latitude, longitude)
    VALUES
    (%(zip)s, %(latitude)s, %(longitude)s)
'''

QUERY_LAT_LONG = '''
select * from locations_data.us_zip_codes where zip = '{}'
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

search_terms = ['starbucks', 'dunkin']

manhattan_zip_codes = [10026, 10027, 10030, 10037, 10039, 10001, 10011, 10018,
10019, 10020, 10036, 10029, 10035, 10010, 10016, 10017, 10022, 10012, 10013, 10014,
10004, 10005, 10006, 10007, 10038, 10280, 10002, 10003, 10009, 10021, 10028,
10044, 10065, 10075, 10128, 10023, 10024, 10025, 10031, 10032, 10033, 10034, 10040]
