# Copyright 2021 The gRPC Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC client-side retry example."""

import json
import logging
import time

import grpc

helloworld_pb2, helloworld_pb2_grpc = grpc.protos_and_services(
    "helloworld.proto"
)


def run():
    # The ServiceConfig proto definition can be found:
    # https://github.com/grpc/grpc-proto/blob/ec886024c2f7b7f597ba89d5b7d60c3f94627b17/grpc/service_config/service_config.proto#L377
    service_config_json = json.dumps(
        {
            "methodConfig": [
                {
                    "name": [
                        {"service": "helloworld.Greeter", "method": "SayHello"}
                    ],
                    "retryPolicy": {
                        "maxAttempts": 5,
                        "initialBackoff": "1s",
                        "maxBackoff": "1s",
                        "backoffMultiplier": 2,
                        "retryableStatusCodes": [
                            "UNAVAILABLE",
                            "RESOURCE_EXHAUSTED",
                            "ABORTED",
                            "INTERNAL",
                            "UNKNOWN"
                        ],
                    },
                }
            ]
        }
    )
    print("Using service config:", service_config_json)
    
    options = [
        ("grpc.enable_retries", 1),
        ("grpc.service_config", service_config_json),
    ]
    
    # Enable debug logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    with grpc.insecure_channel("localhost:50051", options=options) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        print("Starting RPC call...")
        start_time = time.time()
        try:
            # Set timeout to 1.5 seconds
            response = stub.SayHello(
                helloworld_pb2.HelloRequest(name="you"),
                timeout=1.5
            )
            print("Greeter client received: " + response.message)
        except grpc.RpcError as e:
            print(f"RPC failed with status: {e.code()}")
            print(f"Error details: {e.details()}")
            print(f"Debug error string: {e.debug_error_string()}")
        finally:
            total_time = time.time() - start_time
            print(f"Total operation time: {total_time:.2f} seconds")


if __name__ == "__main__":
    run()