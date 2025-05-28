import grpc
import time
import json
import os

# Enable detailed gRPC tracing for debugging
os.environ['GRPC_TRACE'] = 'client_channel,subchannel'
os.environ['GRPC_VERBOSITY'] = 'DEBUG'

import grpc
print(f"DEBUG: gRPC version: {grpc.__version__}")

import greeter_pb2
import greeter_pb2_grpc

def run():
    channel_address = '127.0.0.1:50051' # Standard IPv4, less likely to confuse DNS resolver with "ip://"

    # Define the retry policy
    retry_policy_dict = {
        "methodConfig": [
            {
                "name": [
                    {
                        "service": "greeter.Greeter"
                    }
                ],
                "retryPolicy": {
                    "maxAttempts": 2,
                    "initialBackoff": "0.1s",
                    "maxBackoff": "0.1s",
                    "backoffMultiplier": 1,
                    "retryableStatusCodes": [
                        "UNAVAILABLE"
                    ]
                }
            }
        ]
    }

    # Convert the policy to a JSON string
    service_config_json = json.dumps(retry_policy_dict)
    print(f"DEBUG: Service Config JSON:\n{service_config_json}")
    print(f"DEBUG: Type of service_config_json: {type(service_config_json)}")

    # Create the channel with the service config
    # Use grpc.insecure_channel for direct connection.
    # The 'grpc.service_config' option is the documented way for this.
    with grpc.insecure_channel(
        channel_address, # No 'ipv4:' prefix, let gRPC's default DNS resolve it
        options=[
            ('grpc.enable_retries', True),
            ('grpc.service_config', service_config_json),
        ]
    ) as channel:
        stub = greeter_pb2_grpc.GreeterStub(channel)

        start_time = time.time()
        print(f"\n[Client] Calling SayHello with timeout=1.5s at {start_time:.2f}")
        try:
            response = stub.SayHello(greeter_pb2.HelloRequest(name='World'), timeout=1.5)
            print(f"[Client] Greeter client received: {response.message}")
        except grpc.RpcError as e:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"\n[Client] RPC failed after {elapsed_time:.2f} seconds.")
            print(f"[Client] Error code: {e.code()}")
            print(f"[Client] Error details: {e.details()}")
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print("[Client] **Confirmed: Error was DEADLINE_EXCEEDED**")
            else:
                print(f"[Client] Error was not DEADLINE_EXCEEDED, it was {e.code()}")
        except Exception as e:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"\n[Client] An unexpected error occurred after {elapsed_time:.2f} seconds: {e}")


if __name__ == '__main__':
    run()