import threading
import requests

class Downloader(threading.Thread):
    def __init__(self, url, filename, start_byte, end_byte):
        super().__init__()
        self.url = url
        self.filename = filename
        self.start_byte = start_byte
        self.end_byte = end_byte

    def run(self):
        headers = {'Range': f'bytes={self.start_byte}-{self.end_byte}'}
        response = requests.get(self.url, headers=headers)
        with open(self.filename, 'rb+') as file:
            file.seek(self.start_byte)
            file.write(response.content)

def download_file(url, num_threads=4):
    response = requests.head(url)
    file_size = int(response.headers['Content-Length'])
    chunk_size = file_size // num_threads

    threads = []
    for i in range(num_threads):
        start_byte = i * chunk_size
        end_byte = (i + 1) * chunk_size - 1
        if i == num_threads - 1:
            end_byte = file_size - 1
        thread = Downloader(url, 'file', start_byte, end_byte)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    url = 'https://www.example.com/file.mp4'
    download_file(url)
