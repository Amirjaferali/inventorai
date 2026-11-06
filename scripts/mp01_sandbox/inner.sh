#!/bin/sh
# Runs INSIDE fresh user, mount, pid, net, ipc and uts namespaces created by an
# unprivileged host uid (see run_sandboxed in scripts/mp01_speed_controlled_dcpm_proof.py).
# It builds a root from the pinned image's unpacked filesystem (read-only), adds a
# private /proc, a size-limited /tmp, four device nodes, the MSL checkout (read-only)
# and ONE writable work directory, pivots into it and drops the old root, then
# runs the given command with a cleared environment. The network namespace holds
# only a down loopback interface.
set -eu
ROOTFS="$1"; MSL="$2"; WORK="$3"; shift 3
/usr/bin/mount --bind "$ROOTFS" "$ROOTFS"
/usr/bin/mount -t proc -o nosuid,nodev,noexec proc "$ROOTFS/proc"
/usr/bin/mount -t tmpfs -o size=2g,nosuid,nodev tmpfs "$ROOTFS/tmp"
for d in null zero random urandom; do /usr/bin/mount --bind "/dev/$d" "$ROOTFS/dev/$d"; done
/usr/bin/mount --bind "$MSL" "$ROOTFS/msl"
/usr/bin/mount -o remount,bind,ro "$ROOTFS/msl"
/usr/bin/mount --bind "$WORK" "$ROOTFS/work"
/usr/bin/mount -o remount,bind,ro "$ROOTFS"
cd "$ROOTFS"
/usr/sbin/pivot_root . mnt
cd /work
/usr/bin/umount -l /mnt
exec /usr/bin/env -i HOME=/tmp TMPDIR=/tmp PATH=/usr/bin:/bin LANG=C.UTF-8 "$@"
