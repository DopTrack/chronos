# Doptrack server setup

This folder contains the scripts for setting up the services on the doptack hardware server (doptrack.tudelft.nl).

To set up the services, copy the contents of this folder to the server and run `setup_services.sh`.

The following services will be started:
- MonitorService: sends data to the client when the server status changes
- ControlService: responds to requests of the clients 
- ReceiverService: service to handle mutliple receiver requests from the MonitorService and the ControlService. Problems might occur when the hardware is accessed by both services at the same time.

The two services are secured with certificates. 
- The doptrack server requires server.crt, server.key, and client.crt (not client.key)
- The client/data server requires server.crt, client.key, and client.crt (not server.key)
- The ReceiverService does not require certificates as it will only handle internal connections. It will disconnect services other than coming from 127.0.0.1.

## Sequence diagram for scheduling measurement

```mermaid
sequenceDiagram
autonumber
   participant B as Client Browser
   participant C as Chronos
   participant Doptrack

   B->>C: Provide login credentials 
   activate C 
   C->>B: Serve webpage
   deactivate C

   B->>C: Access scheduler
   activate C
   C->>Doptrack: Check status services
   activate Doptrack
   Doptrack->>C: Return status
   deactivate Doptrack
   C->>B: Serve scheduler
   deactivate C

   B->>C: Schedule measurement
   activate C
   C->>Doptrack: access ControlService
   activate Doptrack
   Doptrack-->Doptrack: Schedule measurement
   Doptrack->>C: Add task to schedule
   deactivate Doptrack
   C->>B: Serve scheduled task
   deactivate C 

```
 