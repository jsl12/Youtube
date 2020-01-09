import os
from datetime import datetime
from pathlib import Path

import googleapiclient.discovery
import yaml
import youtube_dl


class VideoFinder:
    def __init__(self, apikey):
        with open(apikey, 'r') as file:
            apikey = yaml.load(file, Loader=yaml.SafeLoader)['YOUTUBE_API_KEY']
        self.api = googleapiclient.discovery.build('youtube', 'v3', developerKey=apikey)

    def find_channel(self, query):
        res = self.api.search().list(
            part='snippet',
            type='channel',
            q=query
        ).execute()
        return res['items'][0]['snippet']

    def search_channel(self, query, channelId):
        res = self.api.search().list(
            part='snippet',
            type='video',
            channelId=channelId,
            q=query,
            maxResults=50,
            # order='date'
        ).execute()
        return res['items']

    def KEXP_full_performance(self, band_name):
        res = self.search_channel(band_name, self.find_channel('KEXP')['channelId'])
        res = [v for v in res if 'Full Performance' in v['snippet']['title'] and band_name in v['snippet']['title']]
        return res


def download(id, output_dir=None, date_format=None, download=True):
    URL = f'https://www.youtube.com/watch?v={id}'
    output_format = '%(title)s.%(ext)s'
    opts = {'quiet': True, 'outtmpl': output_format}
    with youtube_dl.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(URL, download=False)
        upload_date = datetime.strptime(result['upload_date'], '%Y%m%d')

    date_prefix = upload_date.strftime('%Y-%m-%d_') if date_format is not None else ''

    opts = {
        'quiet': False,
        'merge_output_format': 'mkv',
        'format': 'bestvideo[ext=mp4]+bestaudio',
        'restrict_filenames': True,
        'outtmpl': f'{date_prefix}{output_format}'
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        outfile = Path(ydl.prepare_filename(result))
        print(outfile.name)
        if output_dir is not None:
            os.chdir(Path(output_dir))
        if download:
            return ydl.download([URL])