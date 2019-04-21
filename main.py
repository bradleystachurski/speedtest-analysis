from datetime import datetime
from bokeh.plotting import figure
from bokeh.io import save, output_file
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Div
import pandas as pd

with open('results.txt') as f:
    read_data = f.read()

sep_data = read_data.split('\n\n')


class SpeedTest:
    def __init__(self, date, ping, download, upload):
        self._date = date
        self._ping = ping
        self._download = download
        self._upload = upload

    def __repr__(self):
        return f'Date: {self.date}\nPing: {self.ping}\nDownload: {self.download}\nUpload: {self.upload}'

    @property
    def date(self):
        return self._date

    @property
    def ping(self):
        return self._ping

    @property
    def download(self):
        return self._download

    @property
    def upload(self):
        return self._upload

    @classmethod
    def parse_chunk(cls, chunk):
        if chunk == '':
            return

        split_arr = chunk.split('\n')
        date = SpeedTest.parse_date(split_arr[0])
        ping = SpeedTest.parse_ping(split_arr[1])
        download = SpeedTest.parse_download(split_arr[2])
        upload = SpeedTest.parse_download(split_arr[3])
        return cls(date, ping, download, upload)

    @staticmethod
    def parse_date(date):
        return datetime.strptime(date, '%a %b %d %H:%M:%S %Z %Y')

    @staticmethod
    def parse_ping(ping):
        return ping.split(' ')[1]

    @staticmethod
    def parse_download(download):
        return download.split(' ')[1]

    @staticmethod
    def parse_upload(upload):
        return upload.split(' ')[1]

    @staticmethod
    def format_date(date):
        return date.strftime("%m/%d/%y %H:%M")


data = [SpeedTest.parse_chunk(item) for item in sep_data]

date = []
download = []
upload = []
ping = []
for i in range(len(data)):
    if not data[i]:
        break
    date.append(data[i].date)
    download.append(data[i].download)
    upload.append(data[i].upload)
    ping.append(data[i].ping)


d = {'date': date, 'download': download, 'upload': upload, 'ping': ping}

df = pd.DataFrame(data=d)

df['download'] = pd.to_numeric(df['download'])
df['upload'] = pd.to_numeric(df['upload'])
df['ping'] = pd.to_numeric(df['ping'])

download_summary = df['download'].describe()
upload_summary = df['upload'].describe()
ping_summary = df['ping'].describe()

summary = {
    'stat': download_summary.index,
    'download': download_summary.values,
    'upload': upload_summary.values,
    'ping': ping_summary.values
}

summary_df = pd.DataFrame(summary)
summary_div = Div(text=summary_df.to_html(index=False))

output_file("results.html")
p = figure(x_axis_type='datetime', plot_width=1700)
p.line(date, download, line_width=1)
p.line(date, upload, line_width=1, line_color='red')
save(widgetbox(p, summary_div, sizing_mode='scale_both'))
