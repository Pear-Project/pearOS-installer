"""Real block-device listing for confirm.py's disk-select tab. New
functionality (confirmed with the user) - the original page had this tab's
markup but never populated it with an actual disk list."""
import shlex
import subprocess


def list_disks():
    """Returns [{name, path, size, model}], one entry per whole disk (not
    partitions), via lsblk. Empty list (never raises) if lsblk is missing
    or nothing qualifies - callers should handle zero disks gracefully."""
    try:
        result = subprocess.run(
            # -P: shell-quoted KEY="value" pairs, one disk per line - safe
            # against models/spaces (e.g. "Samsung SSD 970"), unlike lsblk's
            # plain whitespace-separated table output.
            ["lsblk", "-d", "-n", "-b", "-P", "-o", "NAME,SIZE,MODEL,TYPE"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []

    disks = []
    for line in result.stdout.splitlines():
        try:
            fields = dict(tok.split("=", 1) for tok in shlex.split(line))
        except ValueError:
            continue
        if fields.get("TYPE") != "disk":
            continue
        name = fields.get("NAME", "")
        if not name:
            continue
        try:
            size_bytes = int(fields.get("SIZE", "0"))
        except ValueError:
            size_bytes = 0
        if size_bytes <= 0:
            # Unbacked nbd/loop-style device nodes report 0 bytes and are
            # not real installable disks - most systems have a dozen idle
            # nbd0..15 nodes from the kernel module alone.
            continue
        size_gb = size_bytes / (1024 ** 3)
        model = fields.get("MODEL", "").strip()
        disks.append({
            "name": name,
            "path": "/dev/" + name,
            "size": f"{size_gb:.0f} GB",
            "model": model or name,
        })
    return disks
