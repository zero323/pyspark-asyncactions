# asyncactions

A proof of concept asynchronous actions for PySpark using [`concurent.futures`](https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures).


```python
import asyncactions

rdd = sc.range(100)
f = rdd.countAsync()
```