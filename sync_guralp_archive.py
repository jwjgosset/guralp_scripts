import logging
from pathlib import Path
import click
from datetime import datetime, timedelta
from subprocess import Popen, PIPE


def sync_archives(
    source: str,
    archive: str,
    destination: str,
    date: datetime,
    user: str = None,
):
    '''
    Syncs all the expected subdirectories from another acquisition server

    Parameters
    ----------
    source: str
        The IP or hostname of the source acquisiton server

    archive: str
        The path to the parent directory of the archive on the remote server

    destination: str
        The parent directory of the destination archive to sync the source
        archive into

    date: datetime
        The date to sync data for

    user: str
        The user to connect to the remote server as
    '''

    # If a user is specify, make a string that can be attached to the front of
    # the hostname in user@hostname format
    if user is not None:
        user_str = f"{user}@"
    else:
        user_str = ""

    dest_path = Path(destination)

    if not dest_path.exists():
        raise FileNotFoundError(f"Archive directory not found: {destination}")

    source_str = f"{user_str}{source}:"

    datedir_str = date.strftime('%Y/%m/%d')

    for subdir in ['miniseed', 'latency', 'soh']:
        sync_directory(
            subdir=subdir,
            datedir_str=datedir_str,
            source_str=source_str,
            archive=archive,
            destination=destination)

    return


def sync_directory(
    subdir: str,
    datedir_str: str,
    source_str: str,
    archive: str,
    destination: str
):
    '''
    Syncs a particular subdirectory in the archive using rsync

    Parameters
    ----------
    subdir: str
        The subdirectory

    datedir_str: str
        A string for the date-based subdirectory in the format YYYY/MM/DD

    source_str: str
        A string representing the hostname or IP address used to connect to
        the remote archive. Includes username if required. Ex. user@hostname
        or hostname

    archive: str
        The parent directory where the subdirectory is located on the source
        host

    destination: str
        The parent directory where the subdirectory should be synced to
    '''
    # Assemble the rsync command with arguments
    rsync_cmd = ["rsync",
                 "-avR",
                 f"{source_str}{archive}/./{subdir}/{datedir_str}/*",
                 destination]

    # run the rsync command
    proc = Popen(rsync_cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = proc.communicate()

    logging.debug(stdout)

    # Log errors
    logging.error(f'Error running rsync: {str(stderr)}')

    return


@click.command()
@click.option(
    '-s',
    '--source',
    help="The IP or Hostname to sync archive data from",
    required=True,
    type=str
)
@click.option(
    '-u',
    '--user',
    help="The user to connect to the remote host as",
    type=str,
    default=None
)
@click.option(
    '-a',
    '--archive',
    help=("The parent directory of the archive on the remote host. If none " +
          "is specified then the user executing the script is used"),
    type=str,
    required=True
)
@click.option(
    '-d',
    '--destination',
    help=("The destination directory to sync the remote archive into. If " +
          "none is specified, then the same directory is used as on the " +
          "source host"),
    type=str,
    default=None
)
@click.option(
    '-t',
    '--date',
    help=("The date to sync data for, in the format YYYY-MM-DD. If none is " +
          "specificied, yesterday's date is used"),
    type=str,
    default=None
)
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    default=False,
    help='Sets logging level to DEBUG.'
)
def main(
    source: str,
    user: str,
    archive: str,
    destination: str,
    date: str,
    verbose: bool
):
    '''
    Syncs all the expected subdirectories from another acquisition server

    Parameters
    ----------

    source: str
        The IP or hostname of the source acquisiton server

    user: str
        The user to connect to the remote server as

    archive: str
        The path to the parent directory of the archive on the remote server

    destination: str
        The parent directory of the destination archive to sync the source
        archive into

    date: str
        The date to sync data for
    '''
    # Set logging parameters
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if verbose else logging.INFO)

    if date is not None:
        working_date = datetime.strptime(date, '%Y-%m-%d')
    else:
        # If no date specified, use yesterday
        working_date = datetime.today() - timedelta(days=1)

    if destination is None:
        destination = archive

    # Sync the archive from the destination server
    sync_archives(
        source=source,
        archive=archive,
        destination=destination,
        date=working_date,
        user=user
    )


if __name__ == '__main__':
    main()
