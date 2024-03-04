from pathlib import Path
from console_logging.console import Console
LOG = Console()

def verifyFile(files_list):
    return Path(files_list).is_file()

def verifyType(file_name):
    if Path(file_name).is_dir():
        return "dir"
    elif Path(file_name).is_file():
        return "file"
    else:
        return None

def verifyDir(dir_path):
    if not Path(dir_path).exists():
        Path(dir_path).mkdir(parents=True, mode=0o770, exist_ok=True)

def get_current_path():
    return str(Path(__file__).parent.resolve())

def get_absolute_path(relative_path):
    path = Path(relative_path).absolute().as_posix()
    LOG.success('LOAD PATH {:s}'.format(path))
    return path


