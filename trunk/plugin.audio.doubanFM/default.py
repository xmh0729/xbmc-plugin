#sudo apt-get install mpg123
#sudo modprobe snd_bcm2835

import urllib2,urllib,sys,json,os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs

urlFM='http://douban.fm/j/mine/playlist?type=n&channel=0'
addon = xbmcaddon.Addon('plugin.audio.doubanFM')
home = addon.getAddonInfo('path').decode('utf-8')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def get_songs(url):
	songsUrl=[]
	req=urllib2.Request(url)
	fd=urllib2.urlopen(req)
	data=fd.read()
	datajson=json.loads(data)
	songs=datajson.get('song')
	for song in songs:
		#print song.get('title')+" by "+song.get('artist')
		#songsUrl.append(song.get('url'))
		addLink(song.get('url'),song.get('title'),song.get('picture'),song.get('artist'))
	

#os.system('mpg123 --gapless -C'+ ' '.join(songsUrl))

def addLink(url,name,iconimage,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=1"
	print 'url='+u
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Music", infoLabels={ "Title": name, "Plot": description} )
	liz.setProperty( "Fanart_Image", iconimage )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

params=get_params()

url=None
name=None
mode=None

try:
	url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	fanart=urllib.unquote_plus(params["fanart"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
	
if mode==None:
	print "getSongs"
	get_songs(urlFM)

elif mode==1:
	print "setResolvedUrl"
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


xbmcplugin.endOfDirectory(int(sys.argv[1]))