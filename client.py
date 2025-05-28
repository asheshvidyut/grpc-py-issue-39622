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


class RetryLoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        start_time = time.time()
        try:
            print(f"\nMaking request at {time.strftime('%H:%M:%S')}...")
            print(f"Request details: {client_call_details}")
            response = continuation(client_call_details, request)
            elapsed = time.time() - start_time
            print(f"Request succeeded after {elapsed:.2f}s")
            return response
        except grpc.RpcError as e:
            elapsed = time.time() - start_time
            print(f"Request failed after {elapsed:.2f}s with status: {e.code()}")
            print(f"Error details: {e.details()}")
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                print("Retrying due to UNAVAILABLE status...")
            raise


def run():
    # The ServiceConfig proto definition can be found:
    # https://github.com/grpc/grpc-proto/blob/ec886024c2f7b7f597ba89d5b7d60c3f94627b17/grpc/service_config/service_config.proto#L377
    service_config_json = json.dumps(
        {
            "methodConfig": [
                {
                    # To apply retry to all methods, put [{}] in the "name" field
                    "name": [
                        {"service": "helloworld.Greeter", "method": "SayHello"}
                    ],
                    "retryPolicy": {
                        "maxAttempts": 5,
                        "initialBackoff": "0.1s",
                        "maxBackoff": "1s",
                        "backoffMultiplier": 2,
                        "retryableStatusCodes": ["UNAVAILABLE"],
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
        # Add the interceptor to the channel
        channel = grpc.intercept_channel(channel, RetryLoggingInterceptor())
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        print("Starting RPC call...")
        try:
            response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
            print("Greeter client received: " + response.message)
        except grpc.RpcError as e:
            print(f"RPC failed with status: {e.code()}")
            print(f"Error details: {e.details()}")
            print(f"Debug error string: {e.debug_error_string()}")


if __name__ == "__main__":
    run()