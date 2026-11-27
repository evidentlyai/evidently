import contextlib
import ntpath
import os
import posixpath

from fsspec import AbstractFileSystem
from fsspec import get_fs_token_paths
from fsspec.implementations.local import LocalFileSystem


class FSLocation:
    fs: AbstractFileSystem
    path: str

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.fs: AbstractFileSystem
        self.path: str
        self.fs, _, (self.path, *_) = get_fs_token_paths(self.base_path)

    def _resolve_path(self, path: str) -> str:
        if "\x00" in path or posixpath.isabs(path) or ntpath.isabs(path) or ntpath.splitdrive(path)[0]:
            raise ValueError("Path must be relative to the configured base path")

        portable_path = path.replace("\\", "/")
        if any(part == ".." for part in portable_path.split("/")):
            raise ValueError("Path must be relative to the configured base path")

        if path == "":
            fullpath = self.path
        else:
            fullpath = posixpath.normpath(posixpath.join(self.path, path))

        base_path = posixpath.normpath(self.path)
        if base_path not in {"", "."} and posixpath.commonpath((base_path, fullpath)) != base_path:
            raise ValueError("Path must be relative to the configured base path")

        if isinstance(self.fs, LocalFileSystem):
            resolved_base = os.path.realpath(self.path or ".")
            resolved_path = os.path.realpath(fullpath)
            try:
                is_within_base = os.path.commonpath((resolved_base, resolved_path)) == resolved_base
            except ValueError:
                is_within_base = False
            if not is_within_base:
                raise ValueError("Path must be relative to the configured base path")

        return fullpath

    @contextlib.contextmanager
    def open(self, path: str, mode="r"):
        with self.fs.open(self._resolve_path(path), mode) as f:
            yield f

    def makedirs(self, path: str):
        self.fs.makedirs(self._resolve_path(path), exist_ok=True)

    def listdir(self, path: str):
        try:
            fullpath = self._resolve_path(path)
            return [posixpath.relpath(p, fullpath) for p in self.fs.listdir(fullpath, detail=False)]
        except FileNotFoundError:
            return []

    def isdir(self, path: str):
        return self.fs.isdir(self._resolve_path(path))

    def exists(self, path: str):
        return self.fs.exists(self._resolve_path(path))

    def rmtree(self, path: str):
        return self.fs.delete(self._resolve_path(path), recursive=True)

    def invalidate_cache(self, path):
        self.fs.invalidate_cache(self._resolve_path(path))

    def size(self, path):
        return self.fs.size(self._resolve_path(path))
