#!/bin/sh

echo "HOST_UID: ${HOST_UID}"
echo "HOST_GID: ${HOST_GID}"

if [ -n "$HOST_UID" ] && [ -n "$HOST_GID" ]; then
  echo "Creating host user and group with provided UID and GID..."
  addgroup --gid "$HOST_GID" hostgroup
  adduser --disabled-password --gecos '' --uid "$HOST_UID" --gid "$HOST_GID" hostuser
  mkdir -p /uploads
  chown hostuser:hostgroup /uploads
  chmod 755 /uploads
  echo "Running command with host user and group..."
  su-exec hostuser:hostgroup "$@"
else
  echo "Running command without host user and group setup..."
  exec "$@"
fi
