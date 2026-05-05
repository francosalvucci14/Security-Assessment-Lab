import shutil
import time

curr_time = int(time.time())
output = f"/var/backups/backup_{curr_time}"

shutil.make_archive(output, 'zip', "/home/damian")
