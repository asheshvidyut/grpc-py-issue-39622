### Client logs

(venv) asheshvidyut@asheshvidyut:~/grpc-py-issue-39622$ python client.py
/usr/local/google/home/asheshvidyut/grpc-py-issue-39622/venv/lib/python3.12/site-packages/google/protobuf/runtime_version.py:98: UserWarning: Protobuf gencode version 5.27.2 is exactly one major version older than the runtime version 6.31.1 at helloworld.proto. Please update the gencode to avoid compatibility violations in the next runtime release.
  warnings.warn(
Using service config: {"methodConfig": [{"name": [{"service": "helloworld.Greeter", "method": "SayHello"}], "retryPolicy": {"maxAttempts": 5, "initialBackoff": "1s", "maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE", "RESOURCE_EXHAUSTED", "ABORTED", "INTERNAL", "UNKNOWN"]}}]}
Starting RPC call...
RPC failed with status: StatusCode.DEADLINE_EXCEEDED
Error details: Deadline Exceeded
Debug error string: UNKNOWN:Error received from peer  {grpc_status:4, grpc_message:"Deadline Exceeded"}
Total operation time: 1.50 seconds


### Server logs
INFO:root:Received request from ipv6:%5B::1%5D:44340 (attempt 1)
INFO:root:Injecting error to RPC from ipv6:%5B::1%5D:44340 (attempt 1)
INFO:root:Received request from ipv6:%5B::1%5D:44340 (attempt 2)
INFO:root:Injecting error to RPC from ipv6:%5B::1%5D:44340 (attempt 2)
