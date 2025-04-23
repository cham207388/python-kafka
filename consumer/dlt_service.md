
```text
I need a consumer that handles the message from the dlq since the structure has changed a little
message.value() = {original_key: "", original_value: ...}
main_value = message.value().get("original_value")
dl_thread = threading.Thread(target=run_consumer_instance, args=(0,consumer_config,kafka_topic_dlt,))
```

```python
import json
consumer = None
msg = consumer.poll()
msg.key()         # -> b"order-123"  (if you preserved the key)
msg.value()       # -> b'{"original_key": ..., "original_value": ..., "error": ...}'

dl_payload = json.loads(msg.value().decode())

# Now you have:
original_key = dl_payload.get("original_key")
original_value_raw = dl_payload.get("original_value")
error_message = dl_payload.get("error")

# If original_value was JSON, decode it again:
try:
    original_value = json.loads(original_value_raw)
    # process, print or save
except Exception as e:
    original_value = original_value_raw  # If it's just plain text or failed to parse
```
