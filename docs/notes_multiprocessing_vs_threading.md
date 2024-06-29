# Notes

##  notes on when to use multiprocessing vs threading

### Threading
    1. I/O bound tasks (input/output)
        -  tasks that spend most of their time waiting for external events
            Examples:
                - web scraping, reading and writing files
    2. GIL constraints (python) (Global interpreter lock)
        - Prevents multple native threads from executing pythong bytecodes at once.

### Multiprocessing
    1. CPU bound tasks
        - Tasks that require significant CPU processing time 
            Examples: 
                - Image processing, large scale data analysis, mathematical simulation
    2. Avoiding GIL
        - Allows multiple processes to run in parallel, make full use of multi-core CPU's

### Key Differences 
    - Concurrency vs Paralellism