# Notes

##  notes on when to use either threading and concurrent.futures packages

### Threading

- create and manage threads directly
    - offers lower level, more granular control over threads

- Key factors
    1. Direct thread management
        - create, start, join, and manage threads directly
    2. Sychronization primates
        - provides locks, events, conditions, semaphores, and barriers for thread sychronization
            - semaphores: Tools that control access to a resource by maintaining a set number of available slots, used to limit the number of threads accessing a particular resource.
            - barriers: These synchronize multiple threads at a specific point, ensuring that all threads must reach the barrier before any can continue.
    3. grandular control 

- When to use? 
    - Need fine control over thread behavior and sychronization
    - complex scenarios requiring detailed thread management

### Concurrent.futures

- Higher level interface for asychronously executing callables using threads or processes.
    - two main executors:
        1. Threadpool executor
        2. Process pool executor

- Key features
    1. Thread and process pools
        - abstracting away direct thread and process management
    2. Futures objects
        - Represents the result of an asych computation 
    3. Easy to use

- When to use?
    - You want simpler and more convenient
    - Need to run multiple tasks concurrently without worrying about underlying thread of process management.
    - Prefer high level abstraction for common concurrent programming patters. 

### What I used

- Threading used in multiple places instead of concurrent futures.
- It was very simple because of the class structure for running multiple websocket connections. 


