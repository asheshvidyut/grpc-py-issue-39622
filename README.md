### Client logs

```
(venv) asheshvidyut@asheshvidyut:~/grpc-py-issue-39622$ python client.py
Starting RPC call...
RPC failed with status: StatusCode.DEADLINE_EXCEEDED
Error details: Deadline Exceeded
Debug error string: UNKNOWN:Error received from peer  {grpc_status:4, grpc_message:"Deadline Exceeded"}
Total operation time: 1.50 seconds
```

### Server logs
```
INFO:root:Received request from ipv6:%5B::1%5D:44340 (attempt 1)
INFO:root:Injecting error to RPC from ipv6:%5B::1%5D:44340 (attempt 1)
INFO:root:Received request from ipv6:%5B::1%5D:44340 (attempt 2)
INFO:root:Injecting error to RPC from ipv6:%5B::1%5D:44340 (attempt 2)
```
