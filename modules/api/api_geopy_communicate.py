class GetLatLng:
	def __init__(self,address,api_key=None):
		self.address = address
		self.api_key = api_key

	def get_geocoder(sefl,address):
		from  geopy.geocoders import Nominatim
		geolocator = Nominatim()
		loc = geolocator.geocode(address)
		print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)
		return (loc.latitude,loc.longitude)

	def get_google(self,address,api_key=None):
		import requests
		# Set up your Geocoding url
		geocode_url = \
			"https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
		geocode_url = geocode_url \
						+ "&key={}".format(api_key)
		# Ping google for the results
		results = requests.get(geocode_url)
		results = results.json()
		print(results)
		return results
	def getlatlng(self):
		try:
			print("=== Geocoding ===")
			results = self.get_geocoder(self.address)
			return results
		except:
			print("=== Google ===")
			results = self.get_google(self.address,self.api_key)
			return results
		# finally:
		# 	print("=== Not find address ===")
		# 	return ""


# street = "số 17,đường số 3,"
# ward = "phường trường thọ,quận thủ đức"
# city ="Ho Chi Minh"
# country ="Viet Nam"
# address = street+","+ward+","+city+','+ country
# getlatlng = GetLatLng('hoàng viẹt,tân bình')
# getlatlng.getlatlng()