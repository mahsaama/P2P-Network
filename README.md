# Computer-Network-ce443

Summer 1400/2021

- Mahsa Amani
- Mehraneh Najafi
- Saba Hashemi

## About

Implementation of a P2P network. Each peer first connect to admin to get parent port and then will connect to parent. Structure of nodes in this network is like a binary tree. (See the comment in Network.py.)

## Run

First start Admin.py and then run as many instance of Peer you want.

Control the log level with `Debug` value in commons.py.

Some example commands for peer can be seen in test.txt.

Note: This implementation may behave wierdly if any peer get disconnected.

### Commands

Connect to network:

```
CONNECT AS [id_new] ON PORT [port]
```

See known peers (definition: peers that are your childs or parent or have sent packet to you - you can only send packets to these peers):

```
SHOW KNOWN CLIENTS
```

Routing:

```
ROUTE [id_dest]
```

Advertise:

```
ADVERTISE [id_dest|-1]
```

Send hello:

```
Salam Salam Sad Ta Salam [id_dest|-1]
```

Start chat:

```
START CHAT [chat_name]: [id_1] [id_2] ...
```

Exit chat:

```
EXIT CHAT
```

Firewall:

```
FILTER [forward|input|output] [id_src] [id_dest] [type] [accept|drop]
```

 - `type` is packet type number. you can see them in packet.py


Chat firewall:
```
FW CHAT [accept|drop]
```

Check test.txt for examples.
