#!/bin/bash
curl --silent --fail --max-time 3 http://localhost:$PORT/_dash-layout || exit 1