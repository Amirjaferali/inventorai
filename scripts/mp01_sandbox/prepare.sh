#!/bin/sh
# Prepares the isolated stage for scripts/mp01_speed_controlled_dcpm_proof.py.
# A transcription of the commands executed for the v1 evidence (run as the container's
# root, outside the sandbox): retrieve the pinned image by digest without a daemon,
# verify every blob, unpack it, strip setuid / setgid bits, add the sandbox mount
# points, and fetch MSL at the pinned commit.
set -eu
STAGE="${MP01_STAGE:-/srv/mp01}"
REPO=openmodelica/openmodelica
INDEX=sha256:ac9a0223e69b8055d444b42f58ccb9680342b56848c68b81385bf83d7c0ba824
AMD64=sha256:1fa776fd2f03cdcfc03db6f6ac69888dd48c8eca442034495b178dc73b96dc40
MSL_COMMIT=8ae3d35c24e519cb2996cab20f3b13daf2b0c50a
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$STAGE/blobs"
TOKEN=$(curl -sS "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:pull" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
curl -sS -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.oci.image.index.v1+json" \
  -o "$STAGE/blobs/index.json" "https://registry-1.docker.io/v2/$REPO/manifests/$INDEX"
[ "sha256:$(sha256sum "$STAGE/blobs/index.json" | cut -c1-64)" = "$INDEX" ]
curl -sS -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json" \
  -o "$STAGE/blobs/manifest.json" "https://registry-1.docker.io/v2/$REPO/manifests/$AMD64"
[ "sha256:$(sha256sum "$STAGE/blobs/manifest.json" | cut -c1-64)" = "$AMD64" ]
for d in $(python3 -c "import json,sys; m=json.load(open(sys.argv[1])); print(m['config']['digest']); [print(l['digest']) for l in m['layers']]" "$STAGE/blobs/manifest.json"); do
  h=${d#sha256:}
  curl -sS -L -H "Authorization: Bearer $TOKEN" -o "$STAGE/blobs/$h" "https://registry-1.docker.io/v2/$REPO/blobs/$d"
  [ "$(sha256sum "$STAGE/blobs/$h" | cut -c1-64)" = "$h" ]
done
python3 "$HERE/unpack.py" "$STAGE/rootfs" "$STAGE/blobs"
find "$STAGE/rootfs" -xdev -perm /6000 -type f -exec chmod ug-s {} +
for n in null zero random urandom; do : > "$STAGE/rootfs/dev/$n"; done
mkdir -p "$STAGE/rootfs/msl" "$STAGE/rootfs/work" "$STAGE/work"
git init -q "$STAGE/msl"
git -C "$STAGE/msl" remote add origin https://github.com/modelica/ModelicaStandardLibrary
git -C "$STAGE/msl" fetch -q --depth 1 origin "$MSL_COMMIT"
git -C "$STAGE/msl" checkout -q FETCH_HEAD
[ "$(git -C "$STAGE/msl" rev-parse HEAD)" = "$MSL_COMMIT" ]
chmod 755 "$(dirname "$STAGE")" "$STAGE"
echo "stage ready: $STAGE"
