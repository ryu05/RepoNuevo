# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['xmovies8.tv']
        self.base_link = 'http://xmovies8.tv'
        self.search_link = '/movies/search?s=%s'


    def movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(title)

            r = client.request(query)

            t = cleantitle.get(title)

            r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'movie-item-link'}), client.parseDOM(r, 'a', ret='title', attrs = {'class': 'movie-item-link'}))
            r = [(i[0], i[1], re.findall('(\d{4})', i[1])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if len(i[2]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = urlparse.urljoin(self.base_link, r)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            u = urlparse.urljoin(self.base_link, url)

            r = client.request(u)

            r = re.findall("load_player\(\s*'([^']+)'\s*,\s*'?(\d+)\s*'?", r)
            r = list(set(r))
            r = [i for i in r if i[1] == '0' or int(i[1]) >= 720]

            links = []

            for p in r:
                try:
                    headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': u}

                    player = urlparse.urljoin(self.base_link, '/ajax/movie/load_player')

                    post = urllib.urlencode({'id': p[0], 'quality': p[1]})

                    result = client.request(player, post=post, headers=headers)

                    frame = client.parseDOM(result, 'iframe', ret='src')
                    embed = client.parseDOM(result, 'embed', ret='flashvars')

                    if frame:
                        if 'player.php' in frame[0]:
                            frame = client.parseDOM(result, 'input', ret='value', attrs = {'type': 'hidden'})[0]

                            headers = {'Referer': urlparse.urljoin(self.base_link, frame[0])}

                            url = client.request(frame, headers=headers, output='geturl')

                            links += [{'source': 'gvideo', 'url': url, 'quality': directstream.googletag(url)[0]['quality'], 'direct': True}]

                        elif 'openload.' in frame[0]:
                            links += [{'source': 'openload.co', 'url': frame[0], 'quality': 'HD', 'direct': False}]

                        elif 'videomega.' in frame[0]:
                            links += [{'source': 'videomega.tv', 'url': frame[0], 'quality': 'HD', 'direct': False}]

                    elif embed:
                        url = urlparse.parse_qs(embed[0])['fmt_stream_map'][0]

                        url = [i.split('|')[-1] for i in url.split(',')]

                        for i in url:
                            try: links.append({'source': 'gvideo', 'url': i, 'quality': directstream.googletag(i)[0]['quality'], 'direct': True})
                            except: pass

                except:
                    pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Xmovies', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


