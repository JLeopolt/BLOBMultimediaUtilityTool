from threading import Thread, Event


# A thread which has an Event, when the Event is set, the code will stop.
class RevocableThread(Thread):

    def __init__(self, target, pid, isDaemon):
        self.cancel_event = Event()
        super().__init__(target=target, args=[self.cancel_event], daemon=isDaemon)
        self.pid = pid

    # Returns a reference to the event which will cancel this thread.
    def get_cancel_event(self):
        return self.cancel_event

    # Cancels the thread
    # Returns the pid.
    def cancel(self):
        self.cancel_event.set()
        return self.pid


# maintains a single worker thread
class ThreadManager:
    worker_thread = None

    def __init__(self):
        super().__init__()
        self.counter = 0

    # Schedules a worker thread.
    def schedule(self, target):
        self.stop()

        self.counter += 1
        # Create a new worker thread in place of any existing old one.
        self.worker_thread = RevocableThread(target=target, pid=self.counter, isDaemon=True)
        self.worker_thread.start()

    # Returns the stopped thread's PID if successful, otherwise nothing.
    def stop(self):
        # If there is a worker thread already, stop it.
        if self.worker_thread is not None and self.worker_thread.is_alive():
            return self.worker_thread.cancel()
        return
