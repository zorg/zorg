from multiprocessing import Process, Queue
import time


class EventStream(object):

    def __init__(self, settings):
        self.source = settings["source"]
        self.interval = settings["interval"]

        self.queue = Queue()

    def start(self):
        process = Process(target=self.process, args=(self.queue, ))
        process.start()

        self.process = process

        return process

    def stop(self):
        self.process.terminate()

    def process(self, queue):
        while True:
            result = self.source()

            if result == Event.STOP:
                break

            event = Event(
                data=result,
            )

            queue.put(event)

            time.sleep(self.interval)

        queue.put(Event.STOP)


class Event(object):
    STOP = 0xFF

    def __init__(self, data):
        self.data = data

    def serialize(self):
        return "data: %s\n\n" % self.data


class EventsMixin(object):

    def __init__(self, *args, **kwargs):
        self.events = {}
        self.event_streams = {}

        super(EventsMixin, self).__init__(*args, **kwargs)

    def get_event_stream(self, event_name):
        if event_name in self.event_streams:
            return self.event_stream[event_name]

        settings = self.events[event_name]

        event_stream = EventStream(settings)
        event_stream.start()

        return event_stream

    def register_event(self, name, source, interval=0.1):
        self.events[name] = {
            "source": source,
            "interval": interval,
        }

    def serialize(self):
        return {
            "events": self.serialize_events(),
        }

    def serialize_events(self):
        return self.events.keys()
