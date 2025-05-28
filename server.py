import grpc
from concurrent import futures
import time

import greeter_pb2
import greeter_pb2_grpc

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    """Provides methods that implement functionality of greeter server."""
    _request_counter = 0 # To observe attempts

    def SayHello(self, request, context):
        self._request_counter += 1

        # --- FIX STARTS HERE ---
        prev_attempts_meta_val = None
        for key, value in context.invocation_metadata():
            if key == "grpc-previous-rpc-attempts":
                prev_attempts_meta_val = value
                break

        if prev_attempts_meta_val:
            current_attempt_num = int(prev_attempts_meta_val) + 1
        else:
            current_attempt_num = 1
        # --- FIX ENDS HERE ---

        print(f"[Server] Received SayHello request (Attempt {current_attempt_num}) from {request.name} at {time.time():.2f}")

        # Introduce a very small, but explicit, processing delay
        time.sleep(0.01) # 10 milliseconds delay

        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details("Server is currently unavailable. Please retry.")
        print(f"[Server] Responding with UNAVAILABLE at {time.time():.2f}")
        return greeter_pb2.HelloReply()

# In server.py
def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port(f'[::]:{port}') # <--- Make sure this is correct for your server
    server.start()
    print(f"Server started, listening on {port}")
    try:
        while True:
            time.sleep(86400) # Serve for 1 day
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped.")

if __name__ == '__main__':
    serve()