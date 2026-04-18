# HEARTBEAT.md

Goal: run a low-noise caretaker loop.

If everything is fine and nothing needs user attention, reply with exactly:

`HEARTBEAT_OK`

## Responsibilities

- check important local services
- inspect stale or failed task state
- surface only meaningful interruptions
- stay quiet when nothing needs attention
