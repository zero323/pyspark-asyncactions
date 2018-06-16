# asyncactions

A proof of concept asynchronous actions for PySpark using [`concurent.futures`](https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures).


```python
import asyncactions

rdd = sc.range(100)
f = rdd.countAsync()
```

## Disclaimer

Apache Spark, Spark, Apache, and the Spark logo are <a href="https://www.apache.org/foundation/marks/">trademarks</a> of
  <a href="http://www.apache.org">The Apache Software Foundation</a>. This project is not owned, endorsed, or sponsored by The Apache Software Foundation.
