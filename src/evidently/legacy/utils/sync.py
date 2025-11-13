import asyncio
import threading
from functools import wraps
from typing import Awaitable
from typing import Callable
from typing import TypeVar

_loop = asyncio.new_event_loop()
_thr = threading.Thread(target=_loop.run_forever, name="Async Runner", daemon=True)

TA = TypeVar("TA")


def async_to_sync(awaitable: Awaitable[TA]) -> TA:
    try:
        current_loop = asyncio.get_running_loop()
        current_thread = threading.current_thread()

        # Check if we're in a nested call scenario (already in an event loop thread)
        # This includes:
        # 1. We're in _thr running _loop (first level nesting)
        # 2. We're in a nested thread we created (deeper nesting)
        is_nested = (current_loop is _loop and current_thread is _thr) or (
            current_thread is not _thr and current_thread.name.startswith("Async Runner")
        )

        if is_nested:
            # We're already in an event loop thread (either _thr or a nested thread).
            # The problem: if we block on future.result(), the event loop can't
            # process the nested coroutine, causing a deadlock.
            #
            # Solution: Use a separate event loop in a different thread.
            # This allows the nested coroutine to run without blocking the parent loop.
            nested_loop = asyncio.new_event_loop()
            nested_thread = threading.Thread(target=nested_loop.run_forever, name="Async Runner Nested", daemon=True)
            nested_thread.start()
            try:
                # Use the nested loop to run the coroutine
                future = asyncio.run_coroutine_threadsafe(awaitable, nested_loop)
                result = future.result()
                return result
            finally:
                # Clean up: stop the loop and wait for thread to finish
                nested_loop.call_soon_threadsafe(nested_loop.stop)
                nested_thread.join(timeout=1.0)

        # We're in a different thread or different loop (e.g., Jupyter's loop)
        # Use run_coroutine_threadsafe to schedule in _loop
        if not _thr.is_alive():
            _thr.start()
        future = asyncio.run_coroutine_threadsafe(awaitable, _loop)
        result = future.result()
        return result
    except RuntimeError:
        # No running loop, create a new one
        pass
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        return new_loop.run_until_complete(awaitable)
    finally:
        new_loop.close()


def sync_api(f: Callable[..., Awaitable[TA]]) -> Callable[..., TA]:
    @wraps(f)
    def sync_call(*args, **kwargs):
        return async_to_sync(f(*args, **kwargs))

    return sync_call
