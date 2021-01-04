# -*- coding: utf-8 -*-
import re
import requests

import modules.make_up.miscellaneous.normalize.convention as convention
from modules.make_up.miscellaneous.normalize.Price import Price


s1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
s0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"


def remove_accents(input_str):
    s = ""
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s.lower()


def compound2unicode(text):
    text = text.replace("\u0065\u0309", "\u1EBB")    # ẻ
    text = text.replace("\u0065\u0301", "\u00E9")    # é
    text = text.replace("\u0065\u0300", "\u00E8")    # è
    text = text.replace("\u0065\u0323", "\u1EB9")    # ẹ
    text = text.replace("\u0065\u0303", "\u1EBD")    # ẽ
    text = text.replace("\u00EA\u0309", "\u1EC3")    # ể
    text = text.replace("\u00EA\u0301", "\u1EBF")    # ế
    text = text.replace("\u00EA\u0300", "\u1EC1")    # ề
    text = text.replace("\u00EA\u0323", "\u1EC7")    # ệ
    text = text.replace("\u00EA\u0303", "\u1EC5")    # ễ
    text = text.replace("\u0079\u0309", "\u1EF7")    # ỷ
    text = text.replace("\u0079\u0301", "\u00FD")    # ý
    text = text.replace("\u0079\u0300", "\u1EF3")    # ỳ
    text = text.replace("\u0079\u0323", "\u1EF5")    # ỵ
    text = text.replace("\u0079\u0303", "\u1EF9")    # ỹ
    text = text.replace("\u0075\u0309", "\u1EE7")    # ủ
    text = text.replace("\u0075\u0301", "\u00FA")    # ú
    text = text.replace("\u0075\u0300", "\u00F9")    # ù
    text = text.replace("\u0075\u0323", "\u1EE5")    # ụ
    text = text.replace("\u0075\u0303", "\u0169")    # ũ
    text = text.replace("\u01B0\u0309", "\u1EED")    # ử
    text = text.replace("\u01B0\u0301", "\u1EE9")    # ứ
    text = text.replace("\u01B0\u0300", "\u1EEB")    # ừ
    text = text.replace("\u01B0\u0323", "\u1EF1")    # ự
    text = text.replace("\u01B0\u0303", "\u1EEF")    # ữ
    text = text.replace("\u0069\u0309", "\u1EC9")    # ỉ
    text = text.replace("\u0069\u0301", "\u00ED")    # í
    text = text.replace("\u0069\u0300", "\u00EC")    # ì
    text = text.replace("\u0069\u0323", "\u1ECB")    # ị
    text = text.replace("\u0069\u0303", "\u0129")    # ĩ
    text = text.replace("\u006F\u0309", "\u1ECF")    # ỏ
    text = text.replace("\u006F\u0301", "\u00F3")    # ó
    text = text.replace("\u006F\u0300", "\u00F2")    # ò
    text = text.replace("\u006F\u0323", "\u1ECD")    # ọ
    text = text.replace("\u006F\u0303", "\u00F5")    # õ
    text = text.replace("\u01A1\u0309", "\u1EDF")    # ở
    text = text.replace("\u01A1\u0301", "\u1EDB")    # ớ
    text = text.replace("\u01A1\u0300", "\u1EDD")    # ờ
    text = text.replace("\u01A1\u0323", "\u1EE3")    # ợ
    text = text.replace("\u01A1\u0303", "\u1EE1")    # ỡ
    text = text.replace("\u00F4\u0309", "\u1ED5")    # ổ
    text = text.replace("\u00F4\u0301", "\u1ED1")    # ố
    text = text.replace("\u00F4\u0300", "\u1ED3")    # ồ
    text = text.replace("\u00F4\u0323", "\u1ED9")    # ộ
    text = text.replace("\u00F4\u0303", "\u1ED7")    # ỗ
    text = text.replace("\u0061\u0309", "\u1EA3")    # ả
    text = text.replace("\u0061\u0301", "\u00E1")    # á
    text = text.replace("\u0061\u0300", "\u00E0")    # à
    text = text.replace("\u0061\u0323", "\u1EA1")    # ạ
    text = text.replace("\u0061\u0303", "\u00E3")    # ã
    text = text.replace("\u0103\u0309", "\u1EB3")    # ẳ
    text = text.replace("\u0103\u0301", "\u1EAF")    # ắ
    text = text.replace("\u0103\u0300", "\u1EB1")    # ằ
    text = text.replace("\u0103\u0323", "\u1EB7")    # ặ
    text = text.replace("\u0103\u0303", "\u1EB5")    # ẵ
    text = text.replace("\u00E2\u0309", "\u1EA9")    # ẩ
    text = text.replace("\u00E2\u0301", "\u1EA5")    # ấ
    text = text.replace("\u00E2\u0300", "\u1EA7")    # ầ
    text = text.replace("\u00E2\u0323", "\u1EAD")    # ậ
    text = text.replace("\u00E2\u0303", "\u1EAB")    # ẫ
    text = text.replace("\u0045\u0309", "\u1EBA")    # Ẻ
    text = text.replace("\u0045\u0301", "\u00C9")    # É
    text = text.replace("\u0045\u0300", "\u00C8")    # È
    text = text.replace("\u0045\u0323", "\u1EB8")    # Ẹ
    text = text.replace("\u0045\u0303", "\u1EBC")    # Ẽ
    text = text.replace("\u00CA\u0309", "\u1EC2")    # Ể
    text = text.replace("\u00CA\u0301", "\u1EBE")    # Ế
    text = text.replace("\u00CA\u0300", "\u1EC0")    # Ề
    text = text.replace("\u00CA\u0323", "\u1EC6")    # Ệ
    text = text.replace("\u00CA\u0303", "\u1EC4")    # Ễ
    text = text.replace("\u0059\u0309", "\u1EF6")    # Ỷ
    text = text.replace("\u0059\u0301", "\u00DD")    # Ý
    text = text.replace("\u0059\u0300", "\u1EF2")    # Ỳ
    text = text.replace("\u0059\u0323", "\u1EF4")    # Ỵ
    text = text.replace("\u0059\u0303", "\u1EF8")    # Ỹ
    text = text.replace("\u0055\u0309", "\u1EE6")    # Ủ
    text = text.replace("\u0055\u0301", "\u00DA")    # Ú
    text = text.replace("\u0055\u0300", "\u00D9")    # Ù
    text = text.replace("\u0055\u0323", "\u1EE4")    # Ụ
    text = text.replace("\u0055\u0303", "\u0168")    # Ũ
    text = text.replace("\u01AF\u0309", "\u1EEC")    # Ử
    text = text.replace("\u01AF\u0301", "\u1EE8")    # Ứ
    text = text.replace("\u01AF\u0300", "\u1EEA")    # Ừ
    text = text.replace("\u01AF\u0323", "\u1EF0")    # Ự
    text = text.replace("\u01AF\u0303", "\u1EEE")    # Ữ
    text = text.replace("\u0049\u0309", "\u1EC8")    # Ỉ
    text = text.replace("\u0049\u0301", "\u00CD")    # Í
    text = text.replace("\u0049\u0300", "\u00CC")    # Ì
    text = text.replace("\u0049\u0323", "\u1ECA")    # Ị
    text = text.replace("\u0049\u0303", "\u0128")    # Ĩ
    text = text.replace("\u004F\u0309", "\u1ECE")    # Ỏ
    text = text.replace("\u004F\u0301", "\u00D3")    # Ó
    text = text.replace("\u004F\u0300", "\u00D2")    # Ò
    text = text.replace("\u004F\u0323", "\u1ECC")    # Ọ
    text = text.replace("\u004F\u0303", "\u00D5")    # Õ
    text = text.replace("\u01A0\u0309", "\u1EDE")    # Ở
    text = text.replace("\u01A0\u0301", "\u1EDA")    # Ớ
    text = text.replace("\u01A0\u0300", "\u1EDC")    # Ờ
    text = text.replace("\u01A0\u0323", "\u1EE2")    # Ợ
    text = text.replace("\u01A0\u0303", "\u1EE0")    # Ỡ
    text = text.replace("\u00D4\u0309", "\u1ED4")    # Ổ
    text = text.replace("\u00D4\u0301", "\u1ED0")    # Ố
    text = text.replace("\u00D4\u0300", "\u1ED2")    # Ồ
    text = text.replace("\u00D4\u0323", "\u1ED8")    # Ộ
    text = text.replace("\u00D4\u0303", "\u1ED6")    # Ỗ
    text = text.replace("\u0041\u0309", "\u1EA2")    # Ả
    text = text.replace("\u0041\u0301", "\u00C1")    # Á
    text = text.replace("\u0041\u0300", "\u00C0")    # À
    text = text.replace("\u0041\u0323", "\u1EA0")    # Ạ
    text = text.replace("\u0041\u0303", "\u00C3")    # Ã
    text = text.replace("\u0102\u0309", "\u1EB2")    # Ẳ
    text = text.replace("\u0102\u0301", "\u1EAE")    # Ắ
    text = text.replace("\u0102\u0300", "\u1EB0")    # Ằ
    text = text.replace("\u0102\u0323", "\u1EB6")    # Ặ
    text = text.replace("\u0102\u0303", "\u1EB4")    # Ẵ
    text = text.replace("\u00C2\u0309", "\u1EA8")    # Ẩ
    text = text.replace("\u00C2\u0301", "\u1EA4")    # Ấ
    text = text.replace("\u00C2\u0300", "\u1EA6")    # Ầ
    text = text.replace("\u00C2\u0323", "\u1EAC")    # Ậ
    text = text.replace("\u00C2\u0303", "\u1EAA")    # Ẫ
    return text



re_addr1 = r"(\d*.*\d*[^\sa-z\W])"
re_addr2 = r"\d{5,8}"                   # search for the mobile number
def normalize_address(str_addr):
    if str_addr is None or str_addr == "" or re.search(re_addr2, str_addr):
        return None

    str_addr = remove_accents(str_addr)

    print("addr: ", str_addr)
    
    if re.search(re_addr1, str_addr):
        return re.findall(re_addr1, str_addr)[0]
    else:
        return str_addr


def normalize_street(str_street):
    if str_street is None or str_street == "":
        return None

    str_street = re.sub(r"ql",     "quốc lộ",        str_street)
    str_street = re.sub(r"dt|đt",  "đường tỉnh",     str_street)
    str_street = re.sub(r"tl",     "tỉnh lộ",        str_street)
    str_street = re.sub(r"tnhau",  "thoại ngọc hầu", str_street)
    str_street = re.sub(r"hl",     "hương lộ",       str_street)
    str_street = re.sub(r"\d{4,}", "",               str_street)

    return str_street



re_district_1 = r"Q|q\D*(\d{1,2})"
re_district_2 = r"q \. "
def normalize_district(str_district):
    if str_district is None or str_district == "":
        return None

    if re.search(re_district_1, str_district) and re.search(r"\d+", str_district):
        return "quận " + re.search(r"\d+", str_district).group()

    str_district = re.sub(re_district_2, "", str_district)
    str_district = re.sub(r'pn', "phú nhuận", str_district)
    str_district = re.sub(r'tp', "", str_district)
    str_district = re.sub(r'tx', "", str_district)
    str_district = re.sub(r'huy.n', "", str_district)
    str_district = re.sub(r'huy.n', "", str_district)

    return str_district



re_ward_1 = r"p|P|f|F\D*(\d{1,2})"
re_ward_2 = r"f|p \. "
def normalize_ward(str_ward):
    if str_ward is None or str_ward == "":
        return None

    str_ward = str_ward.lower()
    if re.search(re_ward_1, str_ward) and re.search(r"\d+", str_ward):
        return "phường " + re.search(r"\d+", str_ward).group()

    str_ward = re.sub(re_ward_2, "", str_ward)
    str_ward = re.sub(r"hbp", "hiệp bình phước", str_ward)
    str_ward = re.sub(r"xã\s?", "", str_ward)
    str_ward = re.sub(r"btd", "bình trưng đông", str_ward)
    str_ward = re.sub(r"btd", "bình trưng đông", str_ward)


    return str_ward



def normalize_city(str_city):
    '''Return the standardized name of the city
    In this version, it returns the alias names of the city
    '''
    if str_city is None or str_city == "":
        return None
    
    str_city = re.sub(r"tp [\. ]?", "", str_city).lower()
    tmp = str_city
    str_city = remove_accents(str_city)
    
    
    for tag, value in convention.CITIES.items():
        for alias in value['alias']:
            if re.search(alias, str_city):
                return tag
    return tmp


def normalize_position(str_position):
    if str_position is None or str_position == "":
        return None

    str_position = remove_accents(str_position)
    if re.search(r"mat|mt", str_position):
        return "mặt tiền"
    elif re.search(r"hem|ngo|hxh", str_position):
        return "hẻm"
    else:
        return "khác"


def normalize_transaction_type(str_transaction_type):
    '''Return the standardized transaction type
    In this version, it returns the alias names of the transaction
    '''
    if str_transaction_type is None or str_transaction_type == "":
        return None

    tmp = str_transaction_type
    str_transaction_type = remove_accents(str_transaction_type)

    for tag, value in convention.TRANSACTION_TYPE.items():
        for alias in value['aliases']:
            if re.search(alias, str_transaction_type):
                return tag
    return "khác"


def normalize_realestate_type(str_realestate_type):
    '''Return the standardized real estate type
    In this version, it returns the alias names of the real estate
    '''
    if str_realestate_type is None or str_realestate_type == "":
        return None

    tmp = str_realestate_type
    str_realestate_type = remove_accents(str_realestate_type)

    for tag, value in convention.REALESTATE_TYPE.items():
        for alias in value['aliases']:
            if re.search(alias, str_realestate_type):
                return tag

    return "khác"


def normalize_legal(str_legal):
    if str_legal is None or str_legal == "":
        return None

    str_legal = remove_accents(str_legal)

    if re.search(r"hong|sh", str_legal):
        return "sổ hồng"
    elif re.search(r"do|sd", str_legal):
        return "sổ đỏ"
    else:
        return "khác"


def normalize_price(str_price):
    '''Extract price_min, price_max
       May detect that price is of price per meter square or price of the whole real estate
       May detect area 
    
    :Args:
    str_price - string of price extracted by NLP API

    :Returns:
    a 5-element tuple of: (price_min, price_max, price_min_m2, price_min_m2, area), None value may be one of 5 elements in tuple
    '''
    print("Price: ", str_price)
    # basic processing
    str_price = compound2unicode(str_price)

    str_price = re.sub('Mười','10', str_price)
    str_price = re.sub('mười','10', str_price)
    str_price = re.sub('tỏi', 'ty', str_price)

    str_price = remove_accents(str_price)
    
    for number, spelling in convention.NUMBER.items():
        str_price = re.sub(r"\b{}\b".format(spelling), number, str_price)

    # subtitute unconventional spelling name to conventional one
    for conventional, value in convention.NUMBER_CARDINALITY.items():
        for alias in value['aliases']:

            # this command for the case: 33t / m2
            if (alias == 't'or alias == 'tt') and re.search(r"m|m2", str_price):
                str_price = re.sub(r"\b({})\b".format(alias), "trieu", str_price)
            else:
                str_price = re.sub(r"\b({})\b".format(alias), conventional, str_price)

    # remove space
    str_price = re.sub(r'\s','', str_price)
    
   
    # recognize m2, usd
    # we have to check the following condition because in some case the price is "570 tr / 1100 m 2"
    # this price is for the whole 1100-meter-square land, not per meter square
    is_price_m2 = False
    is_usd = False
    area = re.search(r"\d{2,}met|\d{2,}m2|\d{2,}m", str_price)
    if area is None:
        if re.search(r"1metvuong|metvuong|met|m2|m|\d+lo|\d+can", str_price):
            str_price = re.sub(r"1metvuong|metvuong|met|m2|m|\d+lo|\d+can", "", str_price)
            is_price_m2 = True
    else:
        # the price has the form ""800 tr / 191 m 2"
        area = float(re.sub(r"metvuong|met|m2|m", "", area.group()))
        str_price = re.sub(r"\d{2,}met|\d{2,}m2|\d{2,}m", "", str_price)

    for alias in convention.FOREIGN_CURRENCY['usd']:
        if re.search(alias, str_price):
            is_usd = True
            break
    
    
    
    
    
    # split str_price into 2 parts
    for divider in convention.DIVIDERS:
        str_price = re.sub(r"{}".format(divider), convention.MAIN_DIVIDER, str_price)

    str_price_parts = []
    for part in str_price.split(convention.MAIN_DIVIDER):
        if part != '':
            str_price_parts.append(Price(part, is_price_m2, is_usd))

    # each part recognizes itself
    for i in range(len(str_price_parts)):        
        str_price_parts[i].recognize()


    # if one of part are price_m2 or dollar or has biggest cardinality available, set it to the rest
    if len(str_price_parts) > 1:
        # there are 2 parts of price

        # for cardinality, it is a little bit different
        #  if 2 parts have their own biggest cardinality, ignore this case
        #  if part 2 has while part 1 doesn't, 2 parts share the same cardinality
        if str_price_parts[0].get_biggest_cardinality() is None:
            str_price_parts[0].set_biggest_cardinality(str_price_parts[1].get_biggest_cardinality())

    
    # calculate price and print out
    for i in range(len(str_price_parts)):
        str_price_parts[i].calculate_price()
        # str_price_parts[i].debug()
        
        
    
    
    # return results
    if len(str_price_parts) == 0:
        return None, None, None, None, None

    
    price_min    = str_price_parts[0].get_price()
    price_min_m2 = str_price_parts[0].get_price_m2()
    if len(str_price_parts) > 1:
        price_max    = str_price_parts[1].get_price()
        price_max_m2 = str_price_parts[1].get_price_m2()
    else:
        price_max = price_max_m2 = None

    return price_min, price_max, price_min_m2, price_max_m2, area

