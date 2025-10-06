#!/usr/bin/env python3
import os
import shutil
import cgi
import cgitb
from datetime import datetime
import config

cgitb.enable()  # helpful for debugging in browser


def backup_folder(folder_path, keep):
    base_path, folder_name = os.path.split(folder_path.rstrip("/"))
    today = datetime.today().strftime("%Y-%m-%d")
    dst = os.path.join(base_path, f"{folder_name}_{today}")

    if not os.path.exists(folder_path):
        return f"Source folder does not exist: {folder_path}"

    if not os.path.exists(dst):
        shutil.copytree(folder_path, dst)
        result = f"Created backup: {dst}"
    else:
        result = f"Backup already exists for today: {dst}"

    # Clean old backups
    backups = []
    for name in os.listdir(base_path):
        if name.startswith(folder_name + "_"):
            try:
                date_str = name[len(folder_name) + 1 :]
                datetime.strptime(date_str, "%Y-%m-%d")
                backups.append(name)
            except ValueError:
                pass

    backups.sort()
    deleted = []
    while len(backups) > keep:
        old = backups.pop(0)
        old_path = os.path.join(base_path, old)
        shutil.rmtree(old_path)
        deleted.append(old_path)

    if deleted:
        result += f"\nDeleted old backups: {', '.join(deleted)}"
    return result


def main():
    print("Content-Type: text/plain\n")

    form = cgi.FieldStorage()
    key = form.getfirst("key", "")

    if key != config.SECRET_KEY:
        print("Error: Unauthorized. Invalid key.")
        return

    results = []
    for folder in config.FOLDERS:
        results.append(backup_folder(folder, config.KEEP))

    print("\n\n".join(results))


if __name__ == "__main__":
    main()
