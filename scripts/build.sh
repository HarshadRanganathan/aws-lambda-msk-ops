#!/bin/bash
set -euo pipefail

cd $(dirname $0)

echo ">> Building docker image..."

TAG='kafka-ops-lambda'

docker build -t ${TAG} .
