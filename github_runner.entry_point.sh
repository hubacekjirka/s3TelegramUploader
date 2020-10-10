#!/usr/bin/env bash
set -eEuo pipefail

TOKEN=$(curl -s -X POST -H "authorization: token ${PERSONAL_TOKEN}" "https://api.github.com/repos/${OWNER}/${REPO}/actions/runners/registration-token" | jq -r .token)

trap 'cleanup' TERM INT

function cleanup() {
  echo "SIGTERM Received"
  ./config.sh remove --token "${TOKEN}"
}

./config.sh \
  --url "https://github.com/${OWNER}/${REPO}" \
  --token "${TOKEN}" \
  --name "${NAME}" \
  --unattended \
  --work _work

./run.sh &

PID=$!
wait $PID
trap - TERM INT
wait $PID

# We should never get here, leaving only as a reference
cleanup