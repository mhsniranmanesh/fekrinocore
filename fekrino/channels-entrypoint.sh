#!/bin/sh

rm channels.sock.lock
rm channels.sock
daphne -u channels.sock fekrino.asgi:application