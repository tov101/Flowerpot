import time
from machine import Timer


class Scheduler:
    # States
    STATE_IDLE = 0
    STATE_BUSY = 1
    # Vars
    _clock = 0

    _tasks = []
    _nr_of_tasks = 0
    _task_result = False

    _period = None
    _state = STATE_IDLE

    @staticmethod
    def start(timer_period=1000):
        timer = Timer()
        timer.init(period=timer_period, callback=Scheduler.run)

    @staticmethod
    def clock():
        return Scheduler._clock

    @staticmethod
    def add_task(task):
        Scheduler._tasks.append(task)
        Scheduler._nr_of_tasks += 1
        return True

    @staticmethod
    def remove_task(task):
        for _t in Scheduler._tasks:
            if _t == task:
                Scheduler._tasks.pop(task)
                Scheduler._nr_of_tasks -= 1
                return True
        return False

    @staticmethod
    def loop():
        while True:
            # Avoid Interrupt to overlap scheduler main loop
            if Scheduler._state == Scheduler.STATE_BUSY:
                return
            # Mark Scheduler as busy
            Scheduler._state = Scheduler.STATE_BUSY
            # Select and Execute Task
            for task in Scheduler._tasks:
                # I don't need roundRobin for now
                task.run()
            # Free Scheduler
            Scheduler._state = Scheduler.STATE_IDLE
            # Sleep ?!
            time.sleep()

    @staticmethod
    def run(_timer):
        # Increment Clock
        Scheduler._clock += 1


class Task:
    IDLE = 0
    BUSY = 1
    SLEEP = 2

    def __init__(self, period, handler):
        self._executed_cycles = 0
        self._period = period
        self._handler = handler
        self._state = Task.IDLE

        # self.sleep_time = 0

    # def sleep(self, sleep_ticks):
    #     self.sleep_time = sleep_ticks

    def run(self):
        # Do not overlap executions in case that interrupt is faster than execution of task loop
        if self._state == Task.BUSY:
            return

        # Check if it's my time
        _current_tick = Scheduler.clock()
        if _current_tick < self._period:
            return

        _samples = _current_tick // self._period
        if _samples > self._executed_cycles:
            # Store Time
            self._executed_cycles = _samples
            # Call Handler
            self._handler()

        # # Sleep Until self._period time
        # self.sleep_time = self._period - (Scheduler.clock() - _current_tick)
