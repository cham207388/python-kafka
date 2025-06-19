# Errors to research

```bash
%4|1745333196.160|SESSTMOUT|rdkafka#consumer-1| [thrd:main]: Consumer group session timed out (in join-state steady) after 413217 ms without a successful response from the group coordinator (broker 2, last error was Success): revoking assignment and rejoining group
%4|1745333196.160|SESSTMOUT|rdkafka#consumer-2| [thrd:main]: Consumer group session timed out (in join-state steady) after 413449 ms without a successful response from the group coordinator (broker 2, last error was Success): revoking assignment and rejoining group
%5|1745333196.160|REQTMOUT|rdkafka#consumer-2| [thrd:localhost:9092/1]: localhost:9092/1: Timed out FetchRequest in flight (after 410812ms, timeout #0)
%4|1745333196.160|REQTMOUT|rdkafka#consumer-2| [thrd:localhost:9092/1]: localhost:9092/1: Timed out 1 in-flight, 0 retry-queued, 0 out-queue, 0 partially-sent requests
%5|1745333196.160|REQTMOUT|rdkafka#consumer-1| [thrd:localhost:9094/3]: localhost:9094/3: Timed out FetchRequest in flight (after 410813ms, timeout #0)
%4|1745333196.160|REQTMOUT|rdkafka#consumer-1| [thrd:localhost:9094/3]: localhost:9094/3: Timed out 1 in-flight, 0 retry-queued, 0 out-queue, 0 partially-sent requests
%3|1745333196.161|FAIL|rdkafka#consumer-2| [thrd:localhost:9092/1]: localhost:9092/1: 1 request(s) timed out: disconnect (average rtt 501.231ms) (after 3398291ms in state UP)
%3|1745333196.161|FAIL|rdkafka#consumer-1| [thrd:localhost:9094/3]: localhost:9094/3: 1 request(s) timed out: disconnect (average rtt 501.404ms) (after 3398291ms in state UP)
```
