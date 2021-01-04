import re

import modules.make_up.miscellaneous.normalize.convention  as convention



class Price:
    def __init__(self, str_price, is_price_m2, is_usd):
        self.str_price           = str_price
        self.usd                 = is_usd
        self.m2                  = is_price_m2
        self.biggest_cardinality = None
        self.number_list         = []
        ## in structure:
        ## [("14", "ty"), ("75", "trieu")]
        
        self.price               = None
        self.price_m2            = None

    def recognize(self):
        ''' Recognize floating point, digits and cardinality
        '''
        # ****** recognize floatting-point: is point "." or comma ","
        match_point = re.search(r"\.", self.str_price)
        match_comma = re.search(r",", self.str_price)

        if match_comma and match_point is None:
            self.str_price = self.str_price.replace(',', '.')

        # recheck if there are more than a point "." in str_price
        tmp = re.search(r"\.", self.str_price)
        if tmp:
            if tmp.end() - tmp.start() > 1:
                self.str_price = re.sub(r"\.", "", self.str_price)

        if match_comma and match_point:
            # there are both comma and point in str_price

            if match_comma.start() < match_point.start():
                # comma "," stands before point "."
                self.str_price = re.sub(r",", "", self.str_price)
            else:
                # comma "," stands after point "."
                self.str_price = re.sub(r"\.", "", self.str_price)
                self.str_price = re.sub(r",", ".", self.str_price)



        # ****** recognized digit and cardinality
        re_num_cardinality = r"(\d+\.\d+|\d+)(trieu|ty|nghin)?"
        for pair in re.findall(re_num_cardinality, self.str_price):
            self.number_list.append([pair[0], pair[1]])

        # assign biggest cardinality by get the cardinality of the first pair in self.number_list
        try:
            if self.number_list[0][1] != '':
                self.biggest_cardinality = self.number_list[0][1]
        except IndexError:
            self.number_list = []



    def calculate_price(self):
        # fill missing biggest cardinality if it doesnt have
        # check if len of num_list is zero, that means there is not any digit found
        if len(self.number_list) == 0:
            return

        # if reach this step, the biggest cardinality is set
        if self.number_list[0][1] == '':
            self.number_list[0][1] = self.biggest_cardinality

        # fill missing cardinalities of the following if there are more than one number in price
        if len(self.number_list) > 1:
            if self.number_list[1][1] == '':
                if self.number_list[0][1] == 'ty':
                    self.number_list[1][1] = 'trieu'
                elif self.number_list[0][1] == 'trieu':
                    self.number_list[1][1] = 'nghin'

             # fill more 0's to second component of the number
            for i in range(3 - len(self.number_list[1][0])):
                self.number_list[1][0] += '0'

        # calculate price
        price = 0
        for pair in self.number_list:
            number = float(pair[0])
            try:
                cardinality_number = convention.NUMBER_CARDINALITY[pair[1]]['value']
            except KeyError:
                # there is no cardinality word in this case
                cardinality_number = 1

            price += number * cardinality_number

        # if the price is USD
        if self.usd:
            price = price * convention.dollar_vnd_exchange_rate

        if price < convention.LOW_BOUNDARY:
            self.price_m2 = self.price = 0
        else:            
            if self.m2 and price < convention.UP_BOUNDARY:
                # the price is price/m2 not price
                self.price_m2 = price
            else:
                self.m2 = False
                self.price = price


    def get_biggest_cardinality(self):
        return self.biggest_cardinality
    def set_biggest_cardinality(self, cardinality):
        self.biggest_cardinality = cardinality

    def get_price(self):
        return self.price
    def get_price_m2(self):
        return self.price_m2




    def debug(self):
        print("str_price: ", self.str_price)
        print("str_usd: ", self.usd)
        print("str_m2: ", self.m2)
        print("str_biggest_cardinality: ", self.biggest_cardinality)
        print("str_biggest_number_list: ", self.number_list)
        print("price: ", self.price)
        print("price_m2: ", self.price_m2)
        