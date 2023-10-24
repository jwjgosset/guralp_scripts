from datetime import datetime, timedelta
from pathlib import Path
import click
from shutil import copy
from os import remove


def move_soh(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move soh files for the specified date from the guralp cache to the archive
    '''

    # Locate all SOH files for the specified date
    soh_pattern = date.strftime("%Y/*.SOH.%Y.%j")

    soh_files = list(cache_dir.glob(soh_pattern))

    target_dir = archive_dir.joinpath(date.strftime('soh/%Y/%m/%d'))

    # Ensure a folder for the specified date exists in the archive
    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    # Move the files from the cache directory to the archive
    for file in soh_files:
        copy(file, target_dir)
        remove(file)


def move_miniseed(
    cache_dir: Path,
    archive_dir: Path,
    date: datetime
):
    '''
    Move miniseed files for the specified date from the guralp cache to the
    archive
    '''

    # Get a list of all miniseed files for the specified date
    miniseed_files = list(cache_dir.glob((f'{date.year}/*.*.*.*.' +
                                          date.strftime("%Y.%j"))))

    target_dir = archive_dir.joinpath(date.strftime('miniseed/%Y/%m/%d'))

    # Ensure that a directory exists in the archive for the specified date
    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    # Move the files from the cache to the archive
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
    # Get a list of the latency files for the specified date
    latency_files = list(cache_dir.glob('latency/*_*_*_*_' +
                                        date.strftime("%Y_%-j") + '.csv'))

    target_dir = archive_dir.joinpath(date.strftime('latency/%Y/%m/%d'))

    # Ensure a directory for the specified date exists in the archive
    if not target_dir.exists():
        target_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    # Copy the files from the cache to the archive
    for file in latency_files:
        copy(file, target_dir)
        remove(file)


@click.command()
@click.option(
    '-m',
    '--miniseed-dir',
    help='Guralp miniseed cache directory',
    default='/var/cache/guralp/miniseed'
)
@click.option(
    '-l',
    '--latency-dir',
    help='Guralp latency cache directory',
    default='/var/cache/guralp/latency'
)
@click.option(
    '-a',
    '--archive-dir',
    help='Archive directory',
    default='/data/archive'
)
@click.option(
    '-d',
    '--date',
    help='Date',
    default=None
)
def main(
    miniseed_dir: str,
    latency_dir: str,
    archive_dir: str,
    working_date: str
):
    # Get yesterday's date
    if working_date is None:
        working_date = datetime.now() - timedelta(days=1)
    else:
        working_date = datetime.strptime(working_date, '%Y-%m-%d')

    # Move files
    move_soh(
        cache_dir=Path(miniseed_dir),
        archive_dir=Path(archive_dir),
        date=working_date
    )

    move_miniseed(
        cache_dir=Path(miniseed_dir),
        archive_dir=Path(archive_dir),
        date=working_date
    )

    move_latency(
        cache_dir=Path(latency_dir),
        archive_dir=Path(archive_dir),
        date=working_date
    )

    return


if __name__ == '__main__':
    main()
