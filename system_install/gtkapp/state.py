"""Small shared bits: test-mode flag (guards anything that shuts down,
restarts, or otherwise touches the real machine) and the handful of
subprocess calls main.js's IPC handlers made directly."""
import os
import subprocess

IS_TEST_MODE = os.environ.get("SYSTEM_INSTALL_TEST") == "1"


def run_detached(argv):
    try:
        subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        pass


def shutdown():
    if IS_TEST_MODE:
        print("[test mode] would run: shutdown now")
        return
    run_detached(["shutdown", "now"])


def restart():
    if IS_TEST_MODE:
        print("[test mode] would run: shutdown -r now")
        return
    run_detached(["shutdown", "-r", "now"])


def show_log():
    # main.js hardcodes this path (the live session's install log).
    log_path = "/home/liveuser/Desktop/install.log"
    if IS_TEST_MODE:
        print(f"[test mode] would run: kate {log_path}")
        return
    run_detached(["kate", log_path])


def show_disks():
    if IS_TEST_MODE:
        print('[test mode] would run: konsole -e \'$SHELL -c "sudo fdisk -l; $SHELL"\'')
        return
    run_detached(["konsole", "-e", '$SHELL -c "sudo fdisk -l; $SHELL"'])
