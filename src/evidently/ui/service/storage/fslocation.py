import contextlib
import posixpath

from fsspec import AbstractFileSystem
from fsspec import get_fs_token_paths


class FSLocation:
    fs: AbstractFileSystem
    path: str

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.fs: AbstractFileSystem
        self.path: str
        self.fs, _, (self.path, *_) = get_fs_token_paths(self.base_path)

    @contextlib.contextmanager
    def open(self, path: str, mode="r"):
        with self.fs.open(posixpath.join(self.path, path), mode) as f:
            yield f

    def makedirs(self, path: str):
        self.fs.makedirs(posixpath.join(self.path, path), exist_ok=True)

    def listdir(self, path: str):
        try:
            fullpath = posixpath.join(self.path, path)
            return [posixpath.relpath(p, fullpath) for p in self.fs.listdir(fullpath, detail=False)]
        except FileNotFoundError:
            return []

    def isdir(self, path: str):
        return self.fs.isdir(posixpath.join(self.path, path))

    def exists(self, path: str):
        return self.fs.exists(posixpath.join(self.path, path))

    def rmtree(self, path: str):
        return self.fs.delete(posixpath.join(self.path, path), recursive=True)

    def invalidate_cache(self, path):
        self.fs.invalidate_cache(posixpath.join(self.path, path))

    def size(self, path):
        return self.fs.size(posixpath.join(self.path, path))
