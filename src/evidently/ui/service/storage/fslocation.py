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

    def _safe_path(self, path: str) -> str:
        full_path = posixpath.normpath(posixpath.join(self.path, path))
        base_path = posixpath.normpath(self.path)

        if full_path != base_path and not full_path.startswith(base_path + posixpath.sep):
            raise ValueError("Path escapes storage root")

        return full_path


    @contextlib.contextmanager
    def open(self, path: str, mode="r"):
        with self.fs.open(self._safe_path(path), mode) as f:
            yield f

    def makedirs(self, path: str):
        self.fs.makedirs(self._safe_path(path), exist_ok=True)

    def listdir(self, path: str):
        try:
            fullpath = self._safe_path(path)
            return [posixpath.relpath(p, fullpath) for p in self.fs.listdir(fullpath, detail=False)]
        except FileNotFoundError:
            return []

    def isdir(self, path: str):
        return self.fs.isdir(self._safe_path(path))

    def exists(self, path: str):
        return self.fs.exists(self._safe_path(path))

    def rmtree(self, path: str):
        return self.fs.delete(self._safe_path(path), recursive=True)

    def invalidate_cache(self, path):
        self.fs.invalidate_cache(self._safe_path(path))

    def size(self, path: str):
        return self.fs.size(self._safe_path(path))
