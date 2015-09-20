#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

class Vk(VideoExtractor):
    name = 'VK'

    supported_stream_types = ['1080', '720', '480', '360', '240']

    def prepare(self, **kwargs):
        assert self.url
        video_page = get_content(self.url)
        self.title = unescape_html(match1(video_page, '"title":"([^"]+)"'))
        info = dict(re.findall(r'\\"url(\d+)\\":\\"([^"]+)\\"', video_page))
        for quality in self.supported_stream_types:
            if quality in info:
                url = re.sub(r'\\\\\\/', r'/', info[quality])
                _, ext, size = url_info(url)
                self.stream_types.append(quality)
                self.streams[quality] = {'container': ext, 'video_profile': quality, 'src': [url], 'size': size }

site = Vk()
download = site.download_by_url
download_playlist = playlist_not_supported('vk')
