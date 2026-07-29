import os
import shutil
from datetime import datetime

MAX_BACKUPS = 10

def create_backup():

    backup_folder = "backups"

    os.makedirs(
        backup_folder,
        exist_ok=True
    )

    backups = sorted(
        [
            os.path.join(backup_folder, f)
            for f in os.listdir(backup_folder)
            if f.endswith(".db")
        ],
        key=os.path.getmtime
    )

    while len(backups) >= MAX_BACKUPS:

        os.remove(backups[0])

        backups.pop(0)

    timestamp = datetime.now().strftime(
        "%d_%m_%Y_%H_%M_%S"
    )

    backup_file = os.path.join(
        backup_folder,
        f"billing_backup_{timestamp}.db"
    )

    shutil.copy(
        "billing_system.db",
        backup_file
    )

    return backup_file