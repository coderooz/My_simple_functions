import asyncio, threading
import random


class AsyncThreadHandler:
    def __init__(self):
        self.tasks = []

    def create_tasks(self, func):
        pass

    

class AsyncHandlerAio:

    def __init__(self) -> None:
        self.tasks = []

    def create_task(self, task_function, *args, **kwargs) -> None:
        task = asyncio.create_task(task_function(*args, **kwargs))
        self.tasks.append(task)

    async def schedule_task(self, task_function, when, *args, **kwargs):
        """
        Schedule an asynchronous task to be run at a specific time or at regular intervals.

        Parameters:
        - task_function: the function to be run as an asynchronous task
        - when: a float or int specifying the number of seconds in the future to run the task (for a single run) or the number of seconds between runs (for a recurring task)
        - *args: positional arguments to be passed to the task function
        - **kwargs: keyword arguments to be passed to the task function

        Returns:
        - A Task object representing the scheduled task
        """
        # Create a task using the provided task function and arguments
        task = asyncio.create_task(task_function(*args, **kwargs))

        # Schedule the task to be run at the specified time or interval
        if when > 0:
            # Schedule the task to run once in the future
            asyncio.get_event_loop().call_later(when, task)
        elif when < 0:
            # Schedule the task to run repeatedly at a fixed interval
            asyncio.get_event_loop().call_repeatedly(-when, task)
        return task
    
    async def stop_tasks(self):
        # Stop all the asynchronous tasks in the handler as before
        for task in self.tasks:
            task.cancel()
        for task in self.running_tasks:
            task.cancel()
        await asyncio.gather(*(self.tasks + self.running_tasks), return_exceptions=True)
        self.tasks = []
        self.running_tasks = []

    async def run_task(self) -> None:
        while self.tasks:
            while len(self.running_tasks) < self.concurrency and self.tasks:
                task = self.tasks.pop(0)
                self.running_tasks.append(task)
                task.add_done_callback(self.running_tasks.remove)
            await asyncio.wait(self.running_tasks, return_when=asyncio.FIRST_COMPLETED)

    def get_status(self) -> dict:
        """Get the status of the tasks being managed by the handler"""
        return {'pending': len(self.tasks), 'running': len(self.running_tasks)}

if  __name__ == "__main__": 

    async def greet(name):
        print(f"Hello, {name}!")
        sleep_time = random.uniform(0.5, 2.0)  # Generate random sleep time between 0.5 and 2.0 seconds
        await asyncio.sleep(sleep_time)
        print(f"Goodbye, {name}!")

    async def main():
        # Create tasks for two concurrent greetings
        task1 = asyncio.create_task(greet("Alice"))
        task2 = asyncio.create_task(greet("Bob"))

        # Wait for both tasks to complete
        await asyncio.gather(task1, task2)

    # Run the main coroutine
    asyncio.run(main())
