from pathlib import Path

def read_file(file, nbytes=None):
    """
    Read from file. Optionally the first nbytes from the file.
    :param file: file to be read
    :param nbytes: number of bytes to be read
    :return: binary contents of the file
    """
    with open(file, "rb") as f:
        if nbytes is not None:
            data = f.read(nbytes)
        else:
            data = f.read()
    return data

def get_root_directory() -> Path:
    return Path(__file__).parent.parent
