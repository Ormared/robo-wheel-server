import zmq

# ZeroMQ context
context = zmq.Context()

# Socket to talk to clients
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Server is running...")

while True:
    # Wait for the next request from client
    message = socket.recv_json()
    
    dx = message['dx']
    dy = message['dy']
    velocity = message['velocity']
    
    print(f"Received direction: ({dx}, {dy}), velocity: {velocity}")
    
    # Processing can be done here, for example, adjusting car speed, direction etc.
    
    # Send a response back to the client
    response = f"Direction ({dx}, {dy}), velocity {velocity} received"
    socket.send_string(response)

