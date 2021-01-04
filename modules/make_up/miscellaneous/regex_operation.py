from re import search
from re import findall

import datetime

# regex for time
regex_min       = r"min"
regex_hour      = r"hr"
regex_minhour   = r"\d{1,2}"
regex_yesterday = r"Yesterday"
regex_time      = r"\d{1,2}:\d{1,2}(.AM|.PM)?"
regex_datetime1 = r"(\d{1,2}\s[A-Z][a-z]{2,7})\sat\s(\d{1,2}:\d{1,2}(.AM|.PM)?)"     # 25 April at 11:09 AM
regex_datetime2 = r"[A-Z][a-z]{2}.\d.at.\d{1,2}:\d{1,2}(.AM|.PM)?"                   # May 8 at 7:35 PM
regex_datetime3 = r"[A-Z][a-z]{2,7}\s\d{1,2},\s\d{4}"                                # December 29, 2018


# regex for post content
regex_postcontent = r"(This content)"

# regex for link
regex_link        = r"#"

# regex for address
regex_addnum_ward = r"\d[0-9]*"
regex_district    = r"\d+"


# regex for full address
re_fulladdr = r"\S+"



# regex for lat and lng
re_latlng = r"(\d{2,3}.\d{3,})"

def get_postdate(str_date, date_now):
    """
        Get date and time of the time difference between date_now and str_date
    :param str_date: String of date (and time) of post
    :param date_now:  Datetime of current day
    :return: 6-tuple (day, month, year, hour, minute)
    """


    # ********** begin exporting time ************


    # Check "min"
    if  search(regex_min, str_date):
        time_interval = datetime.timedelta(minutes=int(search(regex_minhour, str_date).group()))
        time_interval = date_now - time_interval


    # Check "hr"
    elif search(regex_hour, str_date):
        time_interval = datetime.timedelta(hours=int(search(regex_minhour, str_date).group()))
        time_interval = date_now - time_interval


    # Check "Yesterday"
    elif search(regex_yesterday, str_date):
        time_interval = datetime.datetime.today() - datetime.timedelta(days=1)
        str_time_tmp = search(regex_time, str_date).group()

        try:
            tmp = datetime.datetime.strptime(str_time_tmp, '%H:%M' )
        except ValueError:
            tmp = datetime.datetime.strptime(str_time_tmp, "%I:%M %p")
        time_interval = time_interval.replace(hour=tmp.hour, minute=tmp.minute)


    # Check datetime1
    elif search(regex_datetime1, str_date):
        str_time_tmp = search(regex_datetime1, str_date).group()

        try:
            time_interval = datetime.datetime.strptime(str_time_tmp, '%d %B at %H:%M')
        except ValueError:
            time_interval = datetime.datetime.strptime(str_time_tmp, "%d %B at %I:%M %p")

        time_interval = time_interval.replace(year=date_now.year)


    # Check datetime2
    elif search(regex_datetime2, str_date):
        str_time_tmp = search(regex_datetime2, str_date).group()

        try:
            time_interval = datetime.datetime.strptime(str_time_tmp, '%b %d at %H:%M')
        except ValueError:
            time_interval = datetime.datetime.strptime(str_time_tmp, "%b %d at %I:%M %p")

        time_interval = time_interval.replace(year=date_now.year)


    # Check datetime3
    elif search(regex_datetime3, str_date):
        str_time_tmp = search(regex_datetime3, str_date).group()


        time_interval = datetime.datetime.strptime(str_time_tmp, '%B %d, %Y').replace(hour=date_now.hour, minute=date_now.minute)

    # Case with no time specified
    else:
        time_interval = date_now

    return time_interval.day, time_interval.month, time_interval.year, time_interval.hour, time_interval.minute


def get_latlng(str):
    tmp = findall(pattern=re_latlng, string=str)
    if len(tmp) == 2:
        return tmp[0], tmp[1]
    else:
        return None, None




def verify_postcontent(post_content):
    """
        Check if post content contains special string
    :param post_content: Content of the post
    :return: True: Post content contains specified string(s)
             False: otherwise
    """

    return search(regex_postcontent, post_content) is not None


def verify_link(link):
    return search(regex_link, link) is not None


def clean_addr(str_add):
    """
        To clean adrress number and ward
    :param str_add:
    :return:
    """
    str_ret = str_add.replace("\\\\", "\\")
    if len(str_ret) == 0:
        return ""

    result = search(pattern=regex_district, string=str_ret)
    if result:
        return str(result.group())
    else:
        return str_ret


def clean_district(str_district):
    if len(str_district) == 0:
        return ""

    result = search(pattern=regex_district, string=str_district)
    if result:
        return "quận " + result.group()
    else:
        return str_district


def clean_ward(str_ward):
    if len(str_ward) == 0:
        return ""

    result = search(pattern=regex_district, string=str_ward)
    if result:
        return "phường " + result.group()
    else:
        return str_ward


def clean_full_address(full_addr):
    return findall(pattern=re_fulladdr, string=full_addr)



