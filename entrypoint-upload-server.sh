#!/bin/sh

echo "HOST_UID: ${HOST_UID}"
echo "HOST_GID: ${HOST_GID}"

if [ -n "$HOST_UID" ] && [ -n "$HOST_GID" ]; then
  addgroup -g "$HOST_GID" hostgroup
  adduser -D -u "$HOST_UID" -G hostgroup hostuser

  echo "New user and group created:"
  echo "User: $(id -u hostuser) - Group: $(id -g hostuser)"

  mkdir -p /uploads
  chown hostuser:hostgroup /uploads
  chmod 755 /uploads
  su-exec hostuser:hostgroup "$@"
else
  exec "$@"
fi
