class PostInfo(object):
    def __init__(self):
        self._info = {
            "page":                             None,
            "link":                             None,
            "title":                            None,
            "post_id":                          None,
            "message":                          None,
            "list_user_like":                   None,
            "post_date":                        None,
            "crawled_date":                     None,
            "score":                            None,
            "attr_addr_number":                 None,
            "attr_addr_street":                 None,
            "attr_addr_district":               None,
            "attr_addr_ward":                   None,
            "attr_addr_city":                   None,
            "attr_position":                    None,
            "attr_surrounding":                 None,
            "attr_surrounding_name":            None,
            "attr_surrounding_characteristics": None,
            "attr_transaction_type":            None,
            "attr_realestate_type":             None,
            "attr_potential":                   None,
            "attr_area":                        None,
            "attr_price":                       None,
            "attr_price_min":                   None,
            "attr_price_max":                   None,
            "attr_price_m2" :                   None,
            "attr_interior_floor":              None,
            "attr_interior_room":               None,
            "attr_orientation":                 None,
            "attr_project":                     None,
            "attr_legal":                       None,
            'location_lng':                     None,
            'location_lat':                     None,
            "source":                           "system",

            'address':                          None,
            'city':                             None,
            'bedroom':                          None,
            'bathroom':                         None,

        }

    def get_info(self, key):
        return self._info[key]
        
    def get_info_all(self):
        return self._info

    def set_info(self, key, value):
        self._info[key] = value

    def get_info_for_pushing(self):
        tmp = self._info.copy()
        for x in tmp:
            if tmp[x] is None:
                tmp[x] = ""

        del tmp['price']
        del tmp['address']
        del tmp['city']
        del tmp['usable_area']
        del tmp['bedroom']
        del tmp['bathroom']


        return tmp
