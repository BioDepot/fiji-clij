import argparse
import json
import pathlib
import os
import certifi
import urllib3
from multiprocessing import pool
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", type=pathlib.Path, default=os.getcwd())
parser.add_argument("pattern", type=str)
parser.add_argument("min", type=int, nargs='?', default=0)
parser.add_argument("max", type=int)

ns = parser.parse_args()

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)

output_dir: pathlib.Path = ns.output_dir
os.makedirs(output_dir.resolve(), exist_ok=True)

def downloadUrl(url: str):
    url_obj = urllib3.util.parse_url(url)
    filename = os.path.basename(url_obj.path)
    full_filename = output_dir / filename
    with http.request('GET', url, preload_content=False) as r, open(full_filename.absolute(), 'wb') as out_file: 
        shutil.copyfileobj(r, out_file)
    print("{} downloaded".format(filename), flush=True)


sequence = [ns.pattern % i for i in range(ns.min, ns.max+1)]

with pool.Pool() as p:
    p.map(downloadUrl, sequence)
