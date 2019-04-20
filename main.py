from datetime import datetime
from bokeh.plotting import figure, output_file, save

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

output_file("results.html")
p = figure(x_axis_type='datetime', plot_width=1700)
p.line(date, download, line_width=1)
p.line(date, upload, line_width=1, line_color='red')
save(p)
