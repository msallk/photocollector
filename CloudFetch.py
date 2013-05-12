try:
    import json
except ImportError:
    import simplejson as json 
import urllib
import xml.etree.ElementTree as ET

class CloudFetch:
	def getUrlList(self):
		urllist = []
		fblist = self.getFacebookList()
		twlist = self.getTwitterList()
		iglist = self.getInstagramList()
		flrlist = self.getFlickrList()
		urllist.extend(fblist)
		urllist.extend(twlist)
		urllist.extend(iglist)
		urllist.extend(flrlist)
		print urllist
		return urllist
	def getFacebookList(self):
		res = []
		url = 'https://graph.facebook.com/100323313508668/photos?access_token=CAAGheTK5pzcBAHMu97vvkhrtSzpZAe33K84sqUPq7cddnb6vAB18zCSW0MpAip5jCYs0xQbZA4ytY3kgD3bkLGtDKtDXqqe2McymCdWfyFj038o7aux4B52AbsgV1W1YZC1UfCj1IqkGWB21DuNpo8a5fjAzyn7d2ntY9SfAQZDZD'
		lib = urllib.urlopen(url)
		data = json.loads(lib.read())
		if 'data' not in data:
			return []
		for photo in data['data']:
			res.append(photo['source'])
		return res

	def getTwitterList(self):
		res = []
		url = 'https://api.twitter.com/1/statuses/user_timeline.json?screen_name=CindyChenchen&include_entities=true'
		lib = urllib.urlopen(url)
		data = json.loads(lib.read())
		if len(data)<1:
			return []
		for photo in data:
			if('entities' in photo and 'media' in photo['entities'] and len(photo['entities']['media'])>0 and 'media_url' in photo['entities']['media'][0]):
				res.append(photo['entities']['media'][0]['media_url'])
		return res

	def getInstagramList(self):
		res = []
		url = 'https://api.instagram.com/v1/users/374292499/media/recent/?access_token=374292499.573e90b.1166ba656f20415b8418c31751f7a3f8&count=-1'
		lib = urllib.urlopen(url)
		data = json.loads(lib.read())
		if len(data)<1:
			return []
		for photo in data['data']:
			#if('image' in photo and 'standard_resolution' in photo['image'] and 'url' in photo['image']['standard_resolution']):
			res.append(photo['images']['standard_resolution']['url'])
		print res
		return res


	#JPG is the only tested file format
	def getFlickrList(self):
		res = []
		url = 'http://ycpi-api.flickr.com/services/rest/?method=flickr.photos.search&api_key=b082c9f2535501b8373dc02c5263e3b1&user_id=95628613@N07'
		lib = urllib.urlopen(url)
		data = ET.parse(lib)
		root =  data.getroot()
		for photos in root:
			for photo in photos:
				id = photo.get('id')
				secret = photo.get('secret')
				server = photo.get('server')
				farm = photo.get('farm')
				if (id==None or secret==None or server==None or farm==None):
					continue
				addr = 'http://farm%s.staticflickr.com/%s/%s_%s.jpg'%((farm, server, id, secret))
				res.append(addr)
		print res
		return res


c = CloudFetch()
c.getUrlList()


