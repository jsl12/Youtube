import youtube_dl
from pathlib import Path
import os
if __name__ == '__main__':
    result_base = Path(r'M:\ARCHIVE\Videos\TV\Samurai Jack')
    # URL = r'https://www.adultswim.com/videos/samurai-jack/i'
    output_format = '%(title)s.%(ext)s'
    opts = {
        'quiet': False,
        # 'merge_output_format': 'mkv',
        'format': 'best',
        'restrict_filenames': True,
        'outtmpl': output_format
    }

    eps = [
        # 'i'
        # 'ii',
        # 'iii',
        # 'iv',
        # 'v',
        # 'vi',
        # 'vii',
        # 'viii',
        # 'ix',
        # 'x',
        # 'xi',
        # 'xii',
        # 'xiii'
        # 'xiv',
        # 'xv',
        # 'xvi',
        # 'xvii',
        # 'xviii',
        # 'xix'
        'xx',
        'xxi',
        'xxii',
        'xxiii',
        'xxiv',
        'xxv'
    ]

    os.chdir(result_base)
    for ep in eps:
        URL = f'https://www.adultswim.com/videos/samurai-jack/{ep}'
        with youtube_dl.YoutubeDL(opts) as ydl:
            result = ydl.extract_info(URL, download=False)
            outfile = Path(ydl.prepare_filename(result))
            ydl.download([URL])
            # print(result)