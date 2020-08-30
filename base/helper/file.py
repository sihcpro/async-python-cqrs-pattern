import os


def get_file_extension(filename):
    result = filename.split(".")
    if result == 1:
        raise ValueError(f"File {filename} has no extension")
    return result[-1]


def get_file_name(file_path):
    return os.path.basename(file_path)


def serialize_path(path):
    tmp_path = path
    if tmp_path.startswith("~"):
        tmp_path = os.path.expanduser(tmp_path)
    if not os.path.isabs(tmp_path):
        tmp_path = os.path.realpath(tmp_path)

    (path_head, _) = os.path.split(tmp_path)
    if not os.path.isdir(path_head):
        raise ValueError(f"Path {path} is not valid")

    return tmp_path


def get_valid_file_path(file_path, filename=None, file_exist=True):
    file_path = serialize_path(file_path)

    if os.path.isfile(file_path):
        return file_path
    if file_exist:
        raise ValueError(f"Path {file_path} is a directory, not a file")

    file_path_is_dir = os.path.isdir(file_path)

    if not file_path_is_dir:
        return file_path

    if file_path_is_dir:
        if filename is None or os.path.isdir(os.path.join(file_path, filename)):
            raise ValueError(f"Path {file_path} is a directory, not a file")
        else:
            return os.path.join(file_path, filename)
