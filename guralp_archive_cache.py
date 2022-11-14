#!/usr/bin/python3
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
# TODO: Update and test


def move_soh(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move soh files for the specified date from the guralp cache to the archive
    '''
    soh_pattern = date.strftime("*.SOH.%Y.%j")

    soh_cache = f'{cache_dir}/miniseed/{date.year}/{soh_pattern}'

    target_dir = archive_dir.joinpath(date.strftime('soh/%Y/%M/%d'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    rsync_cmd = f'rsync --remove-source-files -a {soh_cache} {target_dir}'

    subprocess.Popen(rsync_cmd, shell=True)


def move_miniseed(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move miniseed files for the specified date from the guralp cache to the
    archive
    '''
    miniseed_cache = (f'{cache_dir}/miniseed/{date.year}/*.*.*.*.' +
                      date.strftime("%Y.%j"))

    target_dir = archive_dir.joinpath(date.strftime('miniseed/%Y/%M/%d'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    rsync_cmd = f'rsync --remove-source-files -a {miniseed_cache} {target_dir}'

    subprocess.Popen(rsync_cmd, shell=True)


def move_latency(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move latency csv files for the specified date from guralp cache to the
    archive
    '''
    latency_cache = (f'{cache_dir}/latency/{date.year}/*.*.*.*.' +
                     date.strftime("%Y.%j") + '.csv')

    target_dir = archive_dir.joinpath(date.strftime('latency/%Y/%M/%d'))

    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    rsync_cmd = f'rsync --remove-source-files -a {latency_cache} {target_dir}'

    subprocess.Popen(rsync_cmd, shell=True)


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
