'''
    TV Dominicana XBMC Plugin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.		
'''

import os
import string
import sys
import re
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

addon_id = 'plugin.video.tvdominicana'

net = Net()
addon = Addon(addon_id, sys.argv)

#PATHS
AddonPath = addon.get_path()
IconPath = os.path.join(AddonPath, 'icons')

def _decode_callback(matches):
    '''Callback method used by :meth:`decode`.'''
    id = matches.group(1)
    int_base = 10
    if id[0] == 'x':
        id = id.replace('x', '', 1)
        int_base = 16
        
    try:
        return unichr(int(id, int_base))
    except:
        return id


def decode(data):
    return re.sub("&#((\d+)|(x\d+))(;|(?=\s))", _decode_callback, data).strip()

def unescape(text):
    try:
        text = decode(text)
        rep = {'&lt;': '<',
               '&gt;': '>',
               '&quot': '"',
               '&rsquo;': '\'',
               '&acute;': '\'',
               '&nbsp;': ' ',
               '\t':'',
               '%3A':':',
               '%3a':':',
               '%2F':'/',
               '%2f':'/'
               }
        for s, r in rep.items():
            text = text.replace(s, r)
        # this has to be last:
        text = text.replace("&amp;", "&")
    
    #we don't want to fiddle with non-string types
    except TypeError:
        pass

    return text

def str_conv(data):
    if isinstance(data, str):
        # Must be encoded in UTF-8
        data = data.decode('utf8')
	
    import unicodedata
    data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
	
    data = data.decode('string-escape')
        
    return data

    
mode = addon.queries['mode']
url = addon.queries.get('url', '')
title = addon.queries.get('title', '')
img = addon.queries.get('img', os.path.join(IconPath, ''))

menu_items = [ 
    ('Antena Latina', 'al.jpg', 'GetMedia', 'http://www.antenalatina7.com/'),        
    ('CDN', 'cdn.jpg', 'GetMedia', 'http://cdn.com.do/en-vivo/?canal=cdn'),
    ('CDN 2', 'cdn2.jpg', 'GetMedia', 'http://cdn.com.do/en-vivo/?canal=cdn2'),
    ('CDN AM', 'cdnam.jpg', 'GetMedia', 'http://cdn.com.do/en-vivo/?canal=cdnam'),    
    ('CDN FM', 'cdnfm.jpg', 'GetMedia', 'http://cdn.com.do/en-vivo/?canal=cdnfm'),
    ('CerTV', 'certv.jpg', 'GetMedia', 'http://certvdominicana.com/institucional/live/canal4/'),
    ('Color Vision', 'cv.jpg', 'GetMedia', 'http://www.colorvision.do/tv/index.html'),
    ('Digital-15', 'digital15.jpg', 'GetMedia', 'http://emisoradominicana.net/television/category/popular/canalesdominicanos?limit=100'),
    ('Dominican York TV', 'dytv.jpg', 'GetMedia', 'http://www.dominicanyorktv.com/transmision1.php'),
    ('Mia TV', 'miatv.jpg', 'GetMedia', 'http://www.miatelevision.com/'),
    ('Micro Vision', 'mv.jpg', 'GetMedia', 'http://microvision.com.do/micro/tv/jss-sjs.js'),
    ('Musa Vision', 'musatv.jpg', 'GetMedia', 'http://www.musavision.com/'),
    ('Peravia Vision', 'peravia.jpg', 'GetMedia', 'http://peraviavision.tv/peraviaplayer.html'),
    ('Romana TV', 'rt.jpg', 'GetMedia', 'http://www.romanatv42.com/'),
    ('Tele Antillas', 'ta.jpg', 'GetMedia', 'http://www.teleantillas.com.do/senal-en-vivo/'),
    ('Tele Antillas', 'ta.jpg', 'GetMedia', 'http://www.mekstream.com/clients/teleantillas/javascript/mekstream630.js'),
    ('Tele Futuro', 'tf.jpg', 'GetMedia', 'http://telefuturo.com.do/demo/'),
    ('Tele Medios', 'tm.jpg', 'GetMedia', 'http://www.canal25rd.com/ventana/player.html'),
    ('Tele Micro', 'telemicro.jpg', 'GetMedia', 'http://emisoradominicana.net/television/category/popular/canalesdominicanos?limit=100'),
    ('Tele Nord 8', 'tn8.jpg', 'GetMedia', 'http://www.telenord.com.do/index.php/canales/canal8'),
    ('Tele Nord 8', 'tn8.jpg', 'GetMedia', 'http://www.mekstream.com/clients/telenord8/javascript/mekstream.js'),
    ('Tele Nord 10', 'tn10.jpg', 'GetMedia', 'http://www.telenord.com.do/index.php/canales/canal10'),
    ('Tele Nord 10', 'tn10.jpg', 'GetMedia', 'http://www.mekstream.com/clients/telenord10/javascript/mekstream.js'),
    ('Tele Nord 12', 'tn12.jpg', 'GetMedia', 'http://www.telenord.com.do/index.php/canales/canal12'),
    ('Tele Nord 12', 'tn12.jpg', 'GetMedia', 'http://www.mekstream.com/clients/telenord12/javascript/mekstream.js'),
    ('Tele Nord 14', 'tn14.jpg', 'GetMedia', 'http://www.telenord.com.do/index.php/canales/canal14'),
    ('Tele Nord 14', 'tn14.jpg', 'GetMedia', 'http://www.mekstream.com/clients/telenord14/javascript/mekstream.js'),
    ('Tele Sistema', 't11.jpg', 'GetMedia', 'http://telesistema11.com.do/senal-en-vivo/'),
    ('Tele Sistema', 't11.jpg', 'GetMedia', 'http://www.mekstream.com/clients/telesistema/javascript/mekstream650.js'),
    ('Tele Universo', 'tu.jpg', 'GetMedia', 'http://teleuniversotv.com/'),
    ('Valle Vision', 'vv.jpg', 'GetMedia', 'http://vallevisioncanal10.tv/valle/en_vivo.html'),
    ('Yuna Vision', 'yuna.jpg', 'GetMedia', 'http://www.yunavision.com/'),
    ]    
def MainMenu():  #home-page
    
    for (title, icon, mode, url) in menu_items:
        image = os.path.join(IconPath, icon)
        addon.add_directory({'mode': mode, 'title' : title, 'img' : image, 'url' : url, }, {'title': title}, img=image )
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def FormatRtmpNoSwfUrl(streamer, playpath, pageurl):
    if '.flv' in playpath:
        playpath = re.sub('.flv', '', playpath)
    elif '.mp4' in playpath:
        playpath = 'mp4:' + playpath
        
    playable_url = streamer + ' playpath=' + playpath + ' pageUrl=' + pageurl + ' live=true timeout=30'
    
    return playable_url
    
def FormatRtmpSwfUrl(streamer, playpath, swfurl, pageurl):
    
    if pageurl not in swfurl:
        if swfurl[0] != '/':
            swfurl = '/' + swfurl
        swfurl = pageurl + swfurl
        
    playable_url = FormatRtmpNoSwfUrl(streamer, playpath, pageurl) + ' swfUrl=' + swfurl
    
    return playable_url
    
def GetMedia(url):    
    url_content = net.http_GET(url).content
    url_content = str_conv( unescape(url_content) )
    
    playable_url = None
    
    if 'emisoradominicana.net' in url:
        keyword = title.replace(' ','').lower()
        channel_keyword = re.compile('"/television/' + keyword + '(.+?)"').findall(url_content)[0]
        channel_url = 'http://emisoradominicana.net/television/' + keyword + channel_keyword
        channel_content = net.http_GET(channel_url).content
        stream_url = re.compile('<iframe.+?src=\"(.+?)\"').findall(channel_content)[0]
        url_content = net.http_GET('http://emisoradominicana.net' + stream_url).content
        url = 'http://emisoradominicana.net/television/'
        
    if not playable_url:
        stream_info = re.search("<iframe.+?src=[\"'](http://domiplay.net/.+?)[\"']", url_content)
        if stream_info:
            url_content = net.http_GET(stream_info.group(1)).content
            
    if not playable_url:
        stream_info = re.search("<embed type=[\"']application/x\-shockwave\-flash[\"'].+?flashvars=.+?file=(.+?)&.*id=(.+?)&", url_content)
        if stream_info:
            playpath = stream_info.group(2)
            streamer = stream_info.group(1)
            
            playable_url = FormatRtmpNoSwfUrl(streamer, playpath, url)
    
    if not playable_url:
        stream_info = re.search("(?s)type: ['\"]flash['\"].+?src: ['\"](.+?)['\"].+?file: ['\"](.+?)['\"].+?streamer: ['\"](.+?)['\"]", url_content)
        if stream_info:
            swfurl = stream_info.group(1)
            playpath = stream_info.group(2)
            streamer = stream_info.group(3)
            
            playable_url = FormatRtmpSwfUrl(streamer, playpath, swfurl, url)
            
    if not playable_url:
        stream_info = re.search('["\'](http://.+?.m3u8)["\']', url_content)
        if stream_info:
            playable_url = stream_info.group(1)
            
    if not playable_url:
        stream_info = re.search('<embed src=["\'](.+?)["\'].+?type=["\']application/x\-mplayer2["\']', url_content)
        if stream_info:
            playable_url = stream_info.group(1)

    
    if not playable_url:
        if 'mekstream.com' in url:
            swfurl = re.compile("[\"'](http://.+?.swf)[\"']").findall(stream_content)[0]
            streamer = re.compile("[\"']streamer[\"'],[\"'](.+?)[\"']").findall(stream_content)[0]
            
            print streamer
            xmlplaylist = re.search("[\"']playlistfile[\"'],[\"'](.+?)[\"']", stream_content)
            
            if xmlplaylist:
                print xmlplaylist
                xmlplaylist = xmlplaylist.group(1)
                xmlplaylist_content = net.http_GET(xmlplaylist).content
                
                playpath = re.compile('<media:content.+?url="(.+?)".+?/>').findall( xmlplaylist_content)[0]
                page_url = re.compile("<link>(.+?)</link>").findall(xmlplaylist_content)[0]
                
                playable_url = FormatRtmpSwfUrl(streamer, playpath, swfurl, page_url)
                
    if not playable_url:
        stream_info = re.search('src=["\'](http://www.mekstream.com/clients/.+?/javascript/.+?.js)["\']', url_content)
        if stream_info:
            stream_content = net.http_GET(stream_info.group(1)).content
            
            swfurl = re.compile("[\"'](http://.+?.swf)[\"']").findall(stream_content)[0]
            streamer = re.compile("[\"']streamer[\"'],[\"'](.+?)[\"']").findall(stream_content)[0]
            print streamer
            xmlplaylist = re.search("[\"']playlistfile[\"'],[\"'](.+?)[\"']", stream_content)
            
            if xmlplaylist:
                print xmlplaylist
                xmlplaylist = xmlplaylist.group(1)
                xmlplaylist_content = net.http_GET(xmlplaylist).content
                
                playpath = re.compile('<media:content.+?url="(.+?)".+?/>').findall( xmlplaylist_content)[0]
                
                playable_url = FormatRtmpSwfUrl(streamer, playpath, swfurl, url)
    
    if not playable_url:
        stream_info = re.search("(?s)['\"]streamer['\"]: ['\"](.+?)['\"].+?['\"]file['\"]: ['\"](.+?)['\"].+?type: ['\"]flash['\"].+?src: ['\"](.+?)['\"]", url_content)
        if stream_info:
            streamer = stream_info.group(1)
            playpath = stream_info.group(2)
            swfurl = stream_info.group(3)
            
            playable_url = FormatRtmpSwfUrl(streamer, playpath, swfurl, url)
    
    if not playable_url:
        stream_info = re.search("<embed src=['\"](.+?)['\"].+?flashvars=['\"]src=(.+?)&.+?['\"]", url_content)
        if stream_info:
            swfurl = stream_info.group(1)
            streamer = stream_info.group(2)
            
            playable_url = streamer + ' swfUrl=' + swfurl + ' pageUrl=' + url + ' live=true timeout=30'
    
    if not playable_url:
        stream_info = re.search("(?s)['\"]file['\"],['\"](.+?)['\"].+?['\"]streamer['\"],['\"](.+?)['\"]", url_content)
        if stream_info:
            playpath = stream_info.group(1)
            streamer = stream_info.group(2)
            
            playable_url = FormatRtmpNoSwfUrl(streamer, playpath, url)
            
    if not playable_url:
        stream_info = re.search("file: ['\"](rtmp://.+?)['\"]", url_content)
        if stream_info:
            streamer = stream_info.group(1)
            
            playable_url = streamer + ' pageUrl=' + url + ' live=true timeout=30'
            
    if not playable_url:
        stream_info = re.search('<iframe.+?src="(.+?)"', url_content)
        if stream_info:
            stream_content = net.http_GET(stream_info.group(1)).content
            
            streamer = re.compile("[\"']file[\"'], [\"'](.+?)[\"']").findall(stream_content)[0]
            playpath = re.compile("[\"']id[\"'], [\"'](.+?)[\"']").findall(stream_content)[0]
            
            playable_url = streamer + ' playpath=' + playpath + ' live=true timeout=30'
            
    if not playable_url:
        streamer = re.compile("[\"']file[\"'], [\"'](.+?)[\"']").findall(url_content)[0]
        playpath = re.compile("[\"']id[\"'], [\"'](.+?)[\"']").findall(url_content)[0]
        
        playable_url = streamer + ' playpath=' + playpath + ' live=true timeout=30'
            
    if playable_url == None:
        return
    
    print playable_url
    
    listitem = xbmcgui.ListItem()
    listitem.setInfo('video', {'Title': title} )
    listitem.setIconImage(img)
    listitem.setThumbnailImage(img)

    print playable_url
    
    xbmc.Player().play(playable_url, listitem)
        
if mode == 'main': 
    MainMenu()
elif mode == 'GetMedia':
    GetMedia(url)
