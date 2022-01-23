"""DayZ server wrapper."""

from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from multiprocessing import cpu_count
from pathlib import Path
from subprocess import run
from sys import exit
from typing import Iterator

from dzdsu.constants import SERVER_BINARY


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-f', '--config-file', type=Path, default=CONFIG_FILE, metavar='file',
        help='config file path'
    )
    return parser.parse_args()


def main() -> int:
    """Starts the DayZ server."""

    args = get_args()
    config = CaseSensitiveConfigParser()
    config.read(args.config_file)
    binary = Path.cwd() / SERVER_BINARY
    command = [str(binary), *get_parameters(config)]
    completed_process = run(command, check=False)
    return completed_process.returncode


if __name__ == '__main__':
    exit(main())
