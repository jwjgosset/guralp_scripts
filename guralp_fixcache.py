#!/usr/bin/python3
'''
This script is a quick fix for the fact that since the new year one of the
Guralp Datacenters stopped recording miniseed files in the correct folder with
the correct naming format
'''


import argparse
from datetime import datetime, timedelta
from pathlib import Path
# from subprocess import Popen, PIPE
from shutil import copy
from os import remove
# TODO: Update and test


def move_rename_miniseed(
    cache_dir: Path,
    date: datetime
):
    '''
    Move miniseed files for the specified date from the guralp cache to the
    archive
    '''
    miniseed_files = list(
        cache_dir.glob(('miniseed/*_*_*_*_' +
                        date.strftime("%Y_%j" + '.mseed'))))

    target_dir = cache_dir.joinpath(date.strftime('miniseed/%Y'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    for file in miniseed_files:
        destfile = ((str(file.name).split('.'))[0]).replace('_', '.')
        destination = target_dir.joinpath(destfile)
        copy(file, destination)
        remove(file)


def main():
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        '-a',
        '--archive-dir',
        help='Archive directory',
        default='/data/archive'
    )
    argsparser.add_argument(
        '-d',
        '--date',
        help='Date',
        default=None
    )

    args = argsparser.parse_args()

    # Get yesterday's date
    if args.date is None:
        date = datetime.now() - timedelta(days=1)
    else:
        date = datetime.strptime(args.date, '%Y-%m-%d')

    cache_dir = Path(args.cache_dir)

    move_rename_miniseed(
        cache_dir=cache_dir,
        date=date
    )

    return


if __name__ == '__main__':
    main()
