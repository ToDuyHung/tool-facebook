# def get_price(post_info, attributes):
#     if post_info.get_info('attr_price') is not None:
#         return normalize_price(post_info.get_info('attr_price'))
#     else:
#         price_min = 0
#         price_max = 0
#         price_m2  = 0
#         area_tmp  = 0
#         price_str = ""

#         for tmp in attributes['attr_price']:
#             price = normalize_price(tmp)
#             if price_min == 0 and price[0]:
#                 price_str = tmp
#                 price_min = price[0]
#             if price_max == 0 and price[1]:
#                 price_max = price[1]
#             if price_m2 == 0 and price[2]:
#                 price_m2 = price[2]
#             if area_tmp == 0 and price[4]:
#                 area_tmp = price[4]

#         # if reach here that means not any one extracted by NLP API is valueable
#         return price_min, price_max, price_m2, area_tmp, price_str

import requests

from get_addr import add_street_num_to_addr
import re
url = "http://35.240.240.251/api/v1/real-estate-extraction"

re_addr = "Địa chỉ: (\S+ )*"
def get_from_api(post_content):
    request = requests.Session()
    
    headers = {}
    addr = re.search(re_addr,post_content)
    data_list = [addr.group()]
    response = request.post(
            url=url,
            headers=headers,
            json=data_list
            )

    addr = re.search(re_addr,post_content)

    print("\n===text:{}===\n".format(post_content))
    print("\n===matches:{}===\n".format(addr.group()))

    # there are 2 attributes in this list are list rather than single value
    # the reason is for each attribute NPP API may recognise more than just single value, but we dont know which recognised values
    # are correct. So we must check every single one to find the one we need

    data_attrs = {
        "attr_addr_number":                     "",
        "attr_addr_street":                     "",
        "attr_addr_district":                   "",
        "attr_addr_ward":                       "",
        "attr_addr_city":                       "",
        # "attr_position":                        "",
        # "attr_surrounding":                     "",
        # "attr_surrounding_name":                "",
        # "attr_surrounding_characteristics":     "",
        # "attr_transaction_type":                "",
        # "attr_realestate_type":                 "",
        # "attr_potential":                       "",
        # "attr_area":                            [],
        # "attr_price":                           [],
        # "attr_price_m2":                        "",
        # "attr_interior_floor":                  "",
        # "attr_interior_room":                   "",
        # "attr_orientation":                     "",
        # "attr_project":                         "",
        # "attr_legal":                           "",
        # "normal":                               "",
        # "phone":                                "",
        }

    json_response = response.json()
    print("\n\n\n === json_response:{} === \n\n\n".format(json_response))
    for content, i in zip(
            json_response[0]["tags"],
            range(len(
                    json_response[0]["tags"]
                ))
        ):
        if content["type"] == "addr_street" \
            and data_attrs["attr_addr_number"] == "":
            if json_response[0]["tags"][i-1]["type"] == "normal":
                data_attrs["attr_addr_number"] = \
                    add_street_num_to_addr(
                            json_response[0]["tags"][i-1]["content"]
                        )
            data_attrs["attr_addr_street"] = content["content"]
            # data_attrs["attr_addr_street"] = ''
        
        elif content['type'] == "addr_ward" and \
                data_attrs["attr_addr_ward"]=="":
            data_attrs["attr_addr_ward"] = content["content"]

        elif content['type'] == "addr_district" and \
                data_attrs["attr_addr_district"]=="":
            data_attrs["attr_addr_district"] = content["content"]

        elif content['type'] == "addr_city" and \
                data_attrs["attr_addr_city"]=="":
            data_attrs["attr_addr_city"] = content["content"]
        
        

    return data_attrs

get_from_api(
    """
    🌈 SỐNG TẠI BIỆT THỰ NỔI VINHOMES MARINA: LÀM GÌ CŨNG DỄ, ĐẾN ĐÂU CŨNG GẦN
Bên cạnh hệ thống tiện ích nội khu đẳng cấp như bể bơi hướng hồ, sân tập yoga, đường chạy bộ, sân tennis, sân cầu lông, sân tập bóng rổ, khu BBQ, chòi vọng cảnh... Biệt thự nổi Vinhomes Marina còn kết nối thuận tiện với các công trình khác, đáp ứng mọi nhu cầu của cư dân như Bệnh viện Đa khoa Quốc tế Vinmec, Trường học Liên cấp Vinschool, Trung tâm thương mại Aeon Mall.
Không những vậy, nơi đây còn thuộc trục Đại lộ Đông Tây, Đại lộ Võ Nguyên Giáp nên kết nối thuận tiện vào khu vực trung tâm Hải Phòng như Bến xe Cầu Rào, Sân vận động Lạch Tray, Nhà hát lớn, Sân bay Cát Bi, Ủy ban Nhân dân Thành phố, Cảng Hải Phòng…
Nhờ đó, cư dân vừa được trải nghiệm không gian riêng an yên nhưng vẫn thuận tiện kết nối, di chuyển đến mọi nơi. Sống tại Biệt thự nổi Vinhomes Marina: Làm gì cũng dễ, đến đâu cũng gần!
🌈 Đặc biệt, cơ hội nhân đôi đẳng cấp đang chờ đợi các chủ nhân của Biệt thự nổi Vinhomes Marina. Vừa trải nghiệm cuộc sống thượng lưu đẳng cấp, vừa được nhận ngay những ưu đãi hấp dẫn:
✨ Quà tặng VinID Gift Card trị giá lên tới 150 triệu đồng/căn (áp dụng có điều kiện với từng loại căn)
✨ Tặng gói nội thất trị giá 300 triệu đồng/căn đối với các căn biệt thự song lập thuộc NT8,9,10,11 & SH.19 - SH.29
✨ Hỗ trợ vay vốn đến 70% giá bán
✨ Hỗ trợ lãi suất 18 tháng hoặc nhận chiết khấu không vay lên tới 4%
✨ Chính sách thanh toán sớm từ Chủ đầu tư đối với khách hàng thanh toán trước hạn
✨ Hưởng mức lãi suất lên tới 8%/năm trên khoản tiền và số ngày thanh toán sớm
* Các chương trình đi kèm điều kiện cụ thể
#VinhomesMarina #CauRao2 #HaiPhong
---
Vinhomes Marina - Dấu ấn Địa Trung Hải trên đất Cảng phồn vinh!
Tìm hiểu thêm Dự án tại: https://marina.vinhomes.vn/
Hotline: 1800 1179
Email: vhmarina@vinhomes.vn
Địa chỉ: Cầu Rào 2, P. Vĩnh Niệm, Q. Lê Chân, TP. Hải Phòng.
*Thông tin, hình ảnh, các tiện ích trên nội dung này chỉ mang tính chất minh hoạ tương đối và có thể được điều chỉnh theo quyết định của Chủ đầu tư tại từng thời điểm đảm bảo phù hợp quy hoạch và thực tế thi công dự án. Các thông tin, cam kết chính thức sẽ được quy định cụ thể tại Hợp đồng mua bán. Việc quản lý, vận hành và kinh doanh của khu đô thị sẽ theo quy định của Ban quản lý.
    """
    )