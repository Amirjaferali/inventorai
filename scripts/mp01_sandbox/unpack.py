"""Unpack the pinned image's verified layers, in order, applying OCI whiteouts.
Device nodes are skipped (the sandbox binds the few it needs); ownership is not
restored (the sandbox maps one unprivileged uid); setuid / setgid bits are never set
(modes are masked with 0o1777)."""
import json, os, shutil, sys, tarfile
root, blobs = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(blobs, "manifest.json")))
os.makedirs(root, exist_ok=True)
skipped = 0
for layer in man["layers"]:
    path = os.path.join(blobs, layer["digest"].split(":")[1])
    with tarfile.open(path, "r:*") as tar:
        for m in tar.getmembers():
            name = os.path.normpath(m.name).lstrip("/")
            if name.startswith(".."):
                raise SystemExit("unsafe path " + m.name)
            base, leaf = os.path.split(name)
            if leaf == ".wh..wh..opq":
                d = os.path.join(root, base)
                for x in os.listdir(d) if os.path.isdir(d) else []:
                    p = os.path.join(d, x)
                    shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
                continue
            if leaf.startswith(".wh."):
                p = os.path.join(root, base, leaf[4:])
                if os.path.islink(p) or os.path.isfile(p):
                    os.remove(p)
                elif os.path.isdir(p):
                    shutil.rmtree(p)
                continue
            if m.isdev() or m.isfifo():
                skipped += 1
                continue
            target = os.path.join(root, name)
            if (m.isfile() or m.issym() or m.islnk()) and (os.path.lexists(target)):
                if os.path.isdir(target) and not os.path.islink(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
            tar.extract(m, root, set_attrs=False, filter="fully_trusted")
            if m.isfile() or m.isdir():
                os.chmod(target, (m.mode & 0o1777) | (0o755 if m.isdir() else 0o444 if not m.mode & 0o111 else 0o555))
print("unpacked; device nodes skipped:", skipped)
