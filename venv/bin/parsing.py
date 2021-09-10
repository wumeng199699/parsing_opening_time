import re
import datetime
import sys

def check_opening_time(opening_time, date):
    '''
    Check if a given date in the opening time in a bicycle route
    :param opening_time: The formatted opening time range string
    :param date: ISO-8601 formatted date that need to be checked
    '''
    # day to index config, it matches datetime's day index
    day_index = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}
    patterns = {
        "hour": '(?:[0-1][0-9]|2[0-3])',
        "min_sec": '(?:[0-5][0-9])',
        'day': '(?:Sa|Su|Mo|Tu|We|Th|Fr)'
    }

    is_opening = False
    # Check the opening time format, and get the specific time info through reg expression
    # res = re.match(r'(?:(Sa|Su|Mo|Tu|We|Th|Fr) |(Sa|Su|Mo|Tu|We|Th|Fr)-(Sa|Su|Mo|Tu|We|Th|Fr) |)([0-1][0-9]|[2][0-3]):([0-5][0-9])-([0-1][0-9]|[2][0-3]):([0-5][0-9])', t)
    reg_opening_time = re.compile(
        '(?:({day})-({day}) |({day}) |)({hour}):({min_sec})-({hour}):({min_sec})'.format_map(patterns))
    opening_time_vals = re.match(reg_opening_time, opening_time)

    if not opening_time_vals:
        raise RuntimeError('Invalid opening_time foramt')

    # 'Mo 23:48-21:18' => (None, None, 'Mo', '23', '48', '21', '18')
    vals = opening_time_vals.groups()

    # Get the start/end time seconds relative to 0 clock
    start_sec_offset = int(vals[3]) * 3600 + int(vals[4]) * 60
    end_sec_offset = int(vals[5]) * 3600 + int(vals[6]) * 60

    # Check if the time range is valid, as it's not easy to check it in regular expression
    if start_sec_offset > end_sec_offset:
        raise RuntimeError('Invalid time range in opening_time ')

    # Get day info
    start_day = day_index[vals[0]] if vals[0] else -1
    end_day = day_index[vals[1]] if vals[1] else -1
    single_day = day_index[vals[2]] if vals[2] else -1

    # Parse date
    utc_time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%Sz')
    day = utc_time.weekday()
    sec_offset = utc_time.hour * 3600 + utc_time.minute * 60 + utc_time.second

    if (single_day != -1 and single_day == day) \
            or \
            (start_day != -1 and end_day != -1 and ((start_day <= end_day and day >= start_day and day <= end_day) or (start_day > end_day and (day >= start_day or day <= end_day)))) \
            or \
            (start_day == -1 and end_day == -1 and single_day == -1):
        is_opening = sec_offset >= start_sec_offset and sec_offset <= end_sec_offset

    return is_opening