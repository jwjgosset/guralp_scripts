#!/usr/bin/python3
import argparse
from datetime import datetime, timedelta
from pathlib import Path
# from subprocess import Popen, PIPE
from shutil import copy
from os import remove
# TODO: Update and test


def move_soh(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move soh files for the specified date from the guralp cache to the archive
    '''
    soh_pattern = date.strftime("miniseed/%Y/*.SOH.%Y.%j")

    soh_files = list(cache_dir.glob(soh_pattern))

    # soh_cache = f'{cache_dir}/miniseed/{date.year}/{soh_pattern}'

    target_dir = archive_dir.joinpath(date.strftime('soh/%Y/%m/%d'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    for file in soh_files:
        # filename = file.name
        # file.rename(target_dir.joinpath(filename))
        copy(file, target_dir)
        remove(file)

    # rsync_cmd = f'rsync -a {soh_cache} {target_dir}'

    # proc = Popen(rsync_cmd, stdin=PIPE, stdout=PIPE)
    # stdout, stderr = proc.communicate()
    # print(stdout)
    # print(stderr)


def move_miniseed(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move miniseed files for the specified date from the guralp cache to the
    archive
    '''
    miniseed_files = list(cache_dir.glob((f'miniseed/{date.year}/*.*.*.*.' +
                                          date.strftime("%Y.%j"))))

    target_dir = archive_dir.joinpath(date.strftime('miniseed/%Y/%m/%d'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    for file in miniseed_files:

        copy(file, target_dir)
        remove(file)


def move_latency(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move latency csv files for the specified date from guralp cache to the
    archive
    '''
    latency_files = list(cache_dir.glob('latency/*_*_*_*_' +
                                        date.strftime("%Y_%-j") + '.csv'))

    target_dir = archive_dir.joinpath(date.strftime('latency/%Y/%m/%d'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    for file in latency_files:
        copy(file, target_dir)
        remove(file)


def main():
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        '-c',
        '--cache-dir',
        help='Guralp cache directory',
        default='/var/cache/guralp'
    )
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

    archive_dir = args.archive_dir

    # Move files
    move_soh(
        cache_dir=Path(cache_dir),
        archive_dir=Path(archive_dir),
        date=date
    )

    move_miniseed(
        cache_dir=Path(cache_dir),
        archive_dir=Path(archive_dir),
        date=date
    )

    move_latency(
        cache_dir=Path(cache_dir),
        archive_dir=Path(archive_dir),
        date=date
    )

    return


if __name__ == '__main__':
    main()
