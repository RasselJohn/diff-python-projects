#!/usr/bin/env bash

uvicorn src.server:app --host 0.0.0.0 --port "$EXPOSE_PORT" --ws-ping-interval 5 --ws-ping-timeout 5
