import requests

from modules.make_up.miscellaneous.get_addr import add_street_num_to_addr
from modules.api.api_geopy_communicate import GetLatLng

# url = "http://35.240.240.251/api/v1/real-estate-extraction"
url = "http://127.0.0.1:3005/api/v1/real-estate-extraction"

def get_from_api(post_content):
	request = requests.Session()
	data_list = [post_content]
	print("*** \ndata_list:{}\n ***".format(data_list))
	headers = {}

	response = request.post(
			url=url,
			headers=headers,
			json=data_list
			)

	# there are 2 attributes in this list are list rather than single value
	# the reason is for each attribute NPP API may recognise more than just single value, but we dont know which recognised values
	# are correct. So we must check every single one to find the one we need

	data_attrs = {
		"attr_addr_number":						"",
		"attr_addr_street":						"",
		"attr_addr_district":					"",
		"attr_addr_ward":						"",
		"attr_addr_city":						"",
		"attr_position":						"",
		"attr_surrounding":						"",
		"attr_surrounding_name":				"",
		"attr_surrounding_characteristics":		"",
		"attr_transaction_type":				"",
		"attr_realestate_type":					"",
		"attr_potential":						"",
		"attr_area":							[],
		"attr_price":							[],
		"attr_price_m2":						"",
		"attr_interior_floor":					"",
		"attr_interior_room":					"",
		"attr_orientation":						"",
		"attr_project":							"",
		"attr_legal":							"",
		"normal":								"",
		"phone":								"",
		"lat":									"",
		"lng":									"",
		}

	try:
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
			
			elif content['type'] == "position" and \
					data_attrs["attr_position"]=="":
				data_attrs["attr_position"] = content["content"]
			
			elif content['type'] == "surrounding":
				if data_attrs["attr_surrounding_name"] == "":
					data_attrs["attr_surrounding_name"] = content["content"]
				else:
					data_attrs["attr_surrounding_name"] = data_attrs["attr_surrounding_name"] + \
													" , " + content["content"] 
			elif content["type"] == "surrounding_characteristics":
				data_attrs["attr_surrounding_characteristics"] = \
							data_attrs['attr_surrounding_characteristics'] + \
							content["content"]

			elif content['type'] == "transaction_type" and \
					data_attrs["attr_transaction_type"]=="":
				data_attrs["attr_transaction_type"] = content["content"]

			elif content['type'] == "realestate_type" and \
					data_attrs["attr_realestate_type"]=="":
				data_attrs["attr_realestate_type"] = content["content"]

			elif content["type"] == "potential":
				if data_attrs["attr_potential"] == "": 
					data_attrs["attr_potential"] = content["content"]
				else:
					data_attrs["attr_potential"] = data_attrs["attr_potential"] + " , " + \
										 content["content"]

			elif content["type"] == "area":
				data_attrs["attr_area"].append(content["content"])

			elif content["type"] == "price":
				data_attrs["attr_price"].append(content["content"])

			elif content["type"] == "interior_floor":
				if data_attrs["attr_interior_floor"] == "":
					data_attrs["attr_interior_floor"] = content["content"]
				else:
					data_attrs["attr_interior_floor"] = data_attrs["attr_interior_floor"] + " , " \
									+ content["content"]

			elif content["type"] == "interior_room":
				if data_attrs["attr_interior_room"] == "":
					data_attrs["attr_interior_room"] = content["content"]
				else:
					data_attrs["attr_interior_room"] = data_attrs["attr_interior_room"] + " , " \
									+ content["content"]

			elif content["type"] == "orientation" and  \
					data_attrs["attr_orientation"] == "":
				data_attrs["attr_orientation"] = content["content"] 

			elif content["type"] == "project":
				if data_attrs["attr_project"] == "":
					data_attrs["attr_project"] = content["content"]
				else:
					data_attrs["attr_project"] = data_attrs["attr_project"] + " , " \
									+ content["content"]

			elif content["type"] == "legal" and  \
					data_attrs["attr_legal"] == "":
				data_attrs["attr_legal"] = content["content"] 
			else:
				data_attrs["normal"] = content["content"] 
		data_attrs['attr_addr_city'] = data_attrs['attr_addr_city'] \
				if not data_attrs['attr_addr_city'] \
				else  "Ho Chi Minh"
		attr = data_attrs['attr_project'] + ","		 \
			+  data_attrs['attr_addr_number'] + ","	 \
			+  data_attrs['attr_addr_street'] + ","	 \
			+  data_attrs['attr_addr_ward']	 + "," 	 \
			+  data_attrs['attr_addr_district']	+ ","\
			+  data_attrs['attr_addr_city']
		results = GetLatLng(attr).getlatlng()
		print("---- RESULTS-LAT-LNG:{}".format(results))
		data_attrs['lat'] = str(results[0])
		data_attrs['lng'] = str(results[1])
	except:pass
	return data_attrs

# get_from_api("Em cần nhượng phòng gấpĐịa chỉ: 242 Hoàng Hoa Thám,p5, Q. Bình ThạnhPhòng e ở được từ 2-3 người. Phòng có giá 2tr5, có nhà vệ sinh riêng, nước 50k/người, điện 3,5k/kwh. Sát chợ nên ăn uống rất thoải máiSdt 0944296412")