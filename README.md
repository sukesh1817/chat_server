# POST-X Chat Server

A simple multi-threaded socket-based chat server implementation in Python.

## Overview

POST-X Chat Server creates a TCP socket server that allows multiple clients to connect and chat with each other. The server handles each client connection in a separate thread, allowing for concurrent communication between multiple users.

## Features

- Multi-threaded architecture to handle multiple client connections simultaneously
- Welcome message for new connections
- Username registration for each client
- Message broadcasting to all connected clients except the sender
- Graceful disconnection handling with "quit" or "exit" commands

## Requirements

- Python 3.x
- Standard library modules:
  - `threading`
  - `socket`

## Configuration

The server uses the following default configuration:

```python
SERVER_IP = "0.0.0.0"  # Listen on all available interfaces
SERVER_PORT = 1111     # Default port
BUF_SIZE = 2048        # Buffer size for receiving messages
```

You can modify these values in the code to suit your needs.

## Usage

### Starting the Server

1. Save the code to a file named `chat_server.py`
2. Run the server:

```bash
python server.py
```

3. The server will display: `server listening on 0.0.0.0:1111`

### Client Connection

Clients can connect to the server using any TCP socket client, such as Telnet or a custom client application:

```bash
telnet <server_ip> <port>
```

### Server Workflow

1. When a client connects, the server:
   - Logs the connection in the console
   - Sends a welcome message
   - Asks for the client's name
   - Broadcasts messages from this client to all other connected clients

2. Clients can disconnect by typing "quit" or "exit"

## Implementation Details

The server uses a `ChatServer` class that extends Python's `Thread` class to handle client connections. Each new connection spawns a new thread to manage communication with that client, allowing the server to handle multiple clients simultaneously.

## Error Handling

The server includes basic error handling to catch and display connection issues. In case of exceptions, the server will print the error information to the console.

## Extending the Application

This basic implementation can be extended with features such as:

- Private messaging between users
- User authentication
- Persistent chat history
- Chat rooms or channels
- File sharing capabilities
- Command system for administrative tasks

## License

This code is provided as-is for educational purposes.
