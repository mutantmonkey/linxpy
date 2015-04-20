#!/usr/bin/python3
###############################################################################
# linxpy - python uploader for linx.li
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
###############################################################################

import argparse
import json
import os.path
import requests
import sys
import urllib.parse


logpath = os.path.expanduser('~/.local/share/linx.log')
command = os.path.basename(sys.argv[0])

__version__ = "1.0"
user_agent = "linxpy/{}".format(__version__)
upload_path = 'https://linx.li/upload/public/'


def stream_upload(f, total, label="", chunk_size=64*1024, hide_progress=False):
    while True:
        data = f.read(chunk_size)
        if not data:
            sys.stdout.write("\r")
            sys.stdout.write(''.join([' ' for x in label]))
            sys.stdout.write("\r")
            sys.stdout.flush()
            break

        yield data

        if not hide_progress:
            sys.stdout.write("\r{label:40} {progress:7.2%}".format(
                label=label[-40:],
                progress=f.tell() / total))
            sys.stdout.flush()


def unlinx():
    parser = argparse.ArgumentParser(
        description="Remove files that are in the log from linx.li.")
    parser.add_argument('urls', nargs='+', metavar='url')
    args = parser.parse_args()

    delete_keys = {}
    with open(logpath) as f:
        for line in f:
            line = line.split(':')
            delete_keys[line[0]] = line[1]

    for url in args.urls:
        filename = os.path.basename(url)
        if filename not in delete_keys:
            raise Exception("File does not exist in log.")

        r = requests.delete(
            url,
            verify=True,
            headers={
                'X-Delete-Key': delete_keys[filename],
                'User-Agent': user_agent,
            })

        if r.status_code == 200:
            print("{filename}:{resp}".format(
                filename=filename,
                resp=r.text))
        else:
            print("{filename}:{errormsg}".format(
                filename=filename,
                errormsg=r.status_code))


def linx():
    logfile = open(logpath, 'a')

    parser = argparse.ArgumentParser(description="Upload files to linx.li.")
    parser.add_argument(
        '-e', '--expires', type=int, default=0,
        help="The relative expiration time (in seconds) of the file.")
    parser.add_argument(
        '-s', '--no-progress', action='store_true',
        help="Do not show upload progress.")
    parser.add_argument('files', nargs='*', metavar='file')
    args = parser.parse_args()

    if args.files:
        for filename in args.files:
            basename = os.path.basename(filename)
            total = os.path.getsize(filename)

            with open(filename, 'rb') as f:
                try:
                    r = requests.put(
                        upload_path + urllib.parse.quote(basename),
                        verify=True,
                        headers={
                            'Accept': "application/json",
                            'X-File-Expiry': args.expires,
                            'X-Randomized-Barename': True,
                            'User-Agent': user_agent,
                        },
                        data=stream_upload(
                            f, total, label=basename,
                            hide_progress=args.no_progress))
                except KeyboardInterrupt:
                    raise SystemExit

                data = json.loads(r.text)
                print(data['url'])
                logfile.write("{filename}:{delete_key}\n".format(**data))
    else:
        try:
            r = requests.put(
                upload_path,
                verify=True,
                headers={
                    'Accept': "application/json",
                    'X-File-Expiry': args.expires,
                    'User-Agent': user_agent,
                },
                data=sys.stdin.read().encode('utf-8'))
        except KeyboardInterrupt:
            raise SystemExit

        data = json.loads(r.text)
        print(data['url'])
        logfile.write("{filename}:{delete_key}\n".format(**data))
