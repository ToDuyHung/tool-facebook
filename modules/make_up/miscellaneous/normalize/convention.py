# ********* price **********

NUMBER_CARDINALITY = {
    "nghin" : {
        "order" : 3,
        "value" : 1000,
        "aliases" : ["ngan", "nghin", "k"],
    },
    "trieu" : {
        "order" : 2,
        "value" : 1000000,
        "aliases" : ["trieu", "tr"],
    },
    "ty" : {
        "order" : 1,
        "value" : 1000000000,
        "aliases" : ["ti", "ty", "tt", "t", "tyy", "tyr"],
    },
    
}

NUMBER = {
    '1' : 'mot',
    '2' : 'hai',
    '3' : 'ba',
    '4' : 'bon',
    '5' : 'nam',
    '6' : 'sau',
    '7' : 'bay',
    '8' : 'tam',
    '9' : 'chin',
}

FOREIGN_CURRENCY = {
    "usd": ["usd", "dollar", "dola", '\$']
}

MAIN_DIVIDER = '-'
DIVIDERS     = ['toi', 'va', '~', 'hoac', "=>", "->", "-->", "den"]

dollar_vnd_exchange_rate = 23137.75

# if the price if greater than this BOUNDARY, the price is price of real estate, not price per metter square
UP_BOUNDARY = 200000000

LOW_BOUNDARY = 500

CITIES = {
    "hồ chí minh" : {
        "alias"         : [r"ho chi minh", r"hcm", r'sai']
    },
    "đồng nai" : {
        "alias"         : [r"dong nai", r'\. nai', r'dnai']
    },
    "bà rịa - vũng tàu" : {
        "alias"         : [r"ba ria - vung tau", r"brvt", r"ba ria [- ]?vt"]
    }
}

TRANSACTION_TYPE = {
    "mua": {
        "aliases"       : [r"mua"],
    },
    "thuê": {
        "aliases"       : [r"thue"],
    },
    "nhượng": {
        "aliases"       : [r"nhuong", r'sang'],
    },
    "bán": {
        "aliases"       : [r"ban"],
    },
}

REALESTATE_TYPE = {
    'căn hộ' : {
        "aliases" : [r'can ho', r'can', r'building', r'buillding', r'chung cu', r'ch(?! san)', 
                     r'villa', r'vila', r'homestay', r'penthouse', r'biet thu', r'dinh thu', r'chdv']
    },
    'chung cư' : {
        "aliases" : [r'nha tap the']
    },
    'văn phòng' : {
        "aliases" : [r'office', r'officetel', r'cao oc', r'vp', r'toa nha']
    },
    'đất' : {
        "aliases" : [r'nong nghiep', r'trong cay', r'vuon', r'canh tac', r'dat nen', r'nen', r'dat']
    },
    'dự án' : {
        "aliases" : [r'khu do thi', r'kdt', r'tttm', r'trung tam thuong mai', r'nghi duong', r'phuc hop']
    },
    'mặt bằng' : {
        'aliases' : [r'quan', r'mat bang', r'shop', r'kiot', r'kiosk', r'cua hang', r'nha hang', r'mb']
    },
    'kho' : {
        "aliases" : [r'xuong', r'kho']
    },
    'phòng' : {
        "aliases" : [r'phong tro', r'tro[^n][^g]', r'nha tro', r'day tro']
    },
    
    'khách sạn' : {
        "aliases" : [r'khach san', r'hostel', r'hotel', r'nha nghi']
    },
    'nhà' : {
        "aliases" : [r'nha(?!\sxuong|\sbo|\shang|\stro|\syen)', ]
    },

}