import asyncio
import threading


class AsyncManager:
    def __init__(self):
        self._loop = None
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)

    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._ready.set()
        self._loop.run_forever()

    def start(self):
        self._thread.start()
        self._ready.wait()

    def run(self, coro):
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return fut.result()

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()


manager = AsyncManager()
