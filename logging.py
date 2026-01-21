from datetime import datetime
import multiprocessing

class Loging:
    def __init__(self, log_path):
        self.log_path = log_path
        self.queue = multiprocessing.Queue()
        self.process = None
        self._is_running = False

    def __getstate__(self):
        state = self.__dict__.copy()
        state['process'] = None
        return state

    def _queue_writer(self):
        with open(self.log_path, "a", encoding='utf-8') as f:
            while self._is_running:
                line = self.queue.get()
                if line == 'exit':
                    break
                print(line)
                f.write(f"{line}\n")
                f.flush()

    def put_to_queue(self, type_of, line ):
        self.queue.put(f"{str(type_of).upper()} {datetime.now()}: {str(line)}")

    def start(self):
        self._is_running = True
        self.process = multiprocessing.Process(target=self._queue_writer)
        self.process.start()

    def stop(self):
        self.queue.put('exit')
        self._is_running = False
        if self.process:
            self.process.join()
            self.process = None