import uasyncio as asyncio

TASKS = []

def set_global_exception():
    """Allow for exception handling in event loop."""
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

def reschedule_every_s(t):
    """Decorator for a callback that will keep rescheduling itself."""
    def inner_decorator(cb):
        async def wrapped(*args, **kwargs):
            while True:
                await asyncio.sleep(t)
                cb(*args, **kwargs)
        return wrapped
    return inner_decorator

# Add Coros into the Event Loop
async def main():
    set_global_exception() # Debug aid
    for task in TASKS:
        asyncio.create_task(task())
    while True: # run forever
        await asyncio.sleep_ms(1000)

def add_task(task, period):
    task = reschedule_every_s(period)(task)
    TASKS.append(task)

def start():
    # Run the Event Loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
    except asyncio.TimeoutError:
        print("Timed out")
    finally:
        asyncio.new_event_loop()  # Clear retained state

