from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import ttk
import tkinter as tk
import requests
from urllib.parse import urlparse, unquote
import os
import threading
import time

DOWNLOAD_PATH = r'podcasts'
CHUNK = 2 ** 15
n = 1


def normalize(filename):
    """
    normalize the string to a file name
    :param filename:string to normalize
    :return:normalized file name
    """
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in ' !,-']).rstrip()


def is_url(url):
    """
    checks if url is valid
    :param url: the url to check
    :return: True or False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# create webdriver object
driver = webdriver.Chrome()

# open the 'podcastim.org.il' web site
driver.get('https://podcastim.org.il/%d7%9b%d7%9c-%d7%94%d7%aa%d7%97%d7%95%d7%9e%d7%99%d7%9d/')


class App(tk.Tk):
    """
    The main app class, define the tkinter window
    """
    n = 1

    def __init__(self):
        super().__init__()
        # setup
        self.geometry('300x120')
        self.title('Check')
        # set to topmost
        self.attributes('-topmost', 1)
        # set download button
        ttk.Button(self, text='press to download', command=self.get_el).pack()
        # set processing label
        self.by = ttk.Label(self, text='')
        self.by.pack()
        # set summary label
        self.pro = ttk.Label(self, text='')
        self.pro.pack()

    def download(self, url, pod_n=None, name=None):
        """
        download the podcast and save him with his name in a file be crated
        :param url: url for download
        :type url: str
        :param pod_n: the name of the podcast album
        :type pod_n: str
        :param name: the name of the file
        :type name: str
        :return: None
        """
        self.by['text'] = f'{threading.active_count() - 1} files by downloading'  # set processing label
        p_url = urlparse(url)  # for name
        time_out = 8
        # set file name
        filename = normalize(os.path.split(p_url.path)[-1])
        if name:
            filename = f'{normalize(name)}.mp3'
        # set file path
        filepath = os.path.join(DOWNLOAD_PATH, filename)
        if pod_n:
            pod_n = pod_n.replace('-', ' ')
            if not os.path.exists(os.path.join(DOWNLOAD_PATH, pod_n)):
                os.mkdir(os.path.join(DOWNLOAD_PATH, pod_n))
            filepath = os.path.join(os.path.join(DOWNLOAD_PATH, pod_n), filename)

        # downloading...
        try:
            with requests.get(url, stream=True, timeout=time_out) as down:
                down.raise_for_status()
                with open(filepath, 'wb') as file:
                    for chunk in down.iter_content(chunk_size=CHUNK):
                        file.write(chunk)
            self.by['text'] = f'{threading.active_count() - 2} files by downloading'  # set processing label
            self.pro['text'] = f'{self.n} files completed'  # set summary label
            self.n += 1  # set the counter
        except (requests.ConnectionError, requests.Timeout) as o:
            self.pro['text'] = f'error (1) by downloading {filename}\n{o}'
            print(o)
        except RuntimeError:
            self.pro['text'] = f'error (2) by downloading {filename}'
            os.remove(filepath)

    def get_el(self):
        """
        scrape the file name, album name and the file path. and run the download function in a new thread with the
        arguments.
        :return: None
        """
        # get podcast file
        podcast = driver.find_elements(By.CLASS_NAME, r'ppshare__download')[0]
        url = podcast.get_attribute('download')
        # get podcast name
        name = driver.find_element(By.CLASS_NAME, r'ppjs__episode-title')
        # download the podcast in a different thread
        threading.Thread(target=self.download,
                         args=(url, unquote(urlparse(driver.current_url).path[1:-1]), name.text,)).start()


win = App()
win.mainloop()
