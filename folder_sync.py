import os
import sys
import time
import shutil
import hashlib
import logging
from datetime import datetime

"""
->source_folder: The path to the folder we want to mirror.
->replica_folder: The path to the folder that will be the copy.
->interval: How often to check for changes (in seconds).
->log_file: The file where we'll record what the program did.

"""

"""
->sync_folders function keeps a replica folder in sync with a source folder  checks for differences periodically and updates the replica accordingly.
->logging.basic function logs the active repots to the .log file and console
->while loop runs forever keepimg the source and replica in sync.
"""
def sync_folders(source_folder, replica_folder, interval, log_file):
  
  logging.basicConfig(filename=log_file, level=logging.INFO, 
                      format='%(asctime)s - %(levelname)s - %(message)s')
  while True:
    try:
      sync_folders_once(source_folder, replica_folder)
    except Exception as e:
      logging.error(f"Something went wrong during the sync: {e}")
      print(f"Something went wrong during the sync: {e}")
    time.sleep(interval)

"""
->sync-folders-once function performs a single synchronization between two folders.
->if replica file doesn't exist it creates( to the path that would be specifies by the user) during the comman run.
"""
def sync_folders_once(source_folder, replica_folder):

  if not os.path.exists(replica_folder):
    os.makedirs(replica_folder)
    logging.info(f"Created replica folder: {replica_folder}")
    print(f"Created replica folder: {replica_folder}")

  """
  ->walk through every file and folder in the source folder.
  ->find relative path
  """
  for current_source_folder, _, files in os.walk(source_folder):
    relative_path = os.path.relpath(current_source_folder, source_folder)
    current_replica_folder = os.path.join(replica_folder, relative_path)

    if not os.path.exists(current_replica_folder):
      os.makedirs(current_replica_folder)
      logging.info(f"Created directory in replica: {current_replica_folder}")
      print(f"Created directory in replica: {current_replica_folder}")
    
    """
    ->Go through each file in the current source folder
    ->If the file doesn't exist in the replica, or if it exists but is different (check this using a hash), copy it.
    """
    for file in files:
      source_file_path = os.path.join(current_source_folder, file)
      replica_file_path = os.path.join(current_replica_folder, file)
    
      if not os.path.exists(replica_file_path) or \
         get_file_hash(source_file_path) != get_file_hash(replica_file_path):
        shutil.copy2(source_file_path, replica_file_path)
        logging.info(f"Copied file: {source_file_path} -> {replica_file_path}")
        print(f"Copied file: {source_file_path} -> {replica_file_path}")

  """
  ->Clean up the replica folder by removing any files or folders that no longer exist in the source.
  ->find relative path
  ->Construct the corresponding path in the source folder
  ->Check files in curret replica folder
  """
  for current_replica_folder, dirs, files in os.walk(replica_folder):
    relative_path = os.path.relpath(current_replica_folder, replica_folder)
    current_source_folder = os.path.join(source_folder, relative_path)

    for file in files:
      replica_file_path = os.path.join(current_replica_folder, file)
      source_file_path = os.path.join(current_source_folder, file)
      
      """
      ->If the file doesn't exist(has been deleted/removed) in the source, delete it from the replica
      ->Check each subfolder in the current replica folder
      ->If the subfolder doesn't exist in the source, delete it from the replica
      """
      if not os.path.exists(source_file_path):
        os.remove(replica_file_path)
        logging.info(f"Removed file: {replica_file_path}")
        print(f"Removed file: {replica_file_path}")
  
    for dir in dirs:
      replica_dir_path = os.path.join(current_replica_folder, dir)
      source_dir_path = os.path.join(current_source_folder, dir)

      if not os.path.exists(source_dir_path):
        shutil.rmtree(replica_dir_path)
        logging.info(f"Removed directory: {replica_dir_path}")
        print(f"Removed directory: {replica_dir_path}")

  """
  ->get_file_hash function calculates a unique hash of a file make sure they are identical.
  ->filename: The path to the file.
  """
def get_file_hash(filename):
  with open(filename, "rb") as f:
    file_hash = hashlib.md5()
    while chunk := f.read(8192):
      file_hash.update(chunk)
  return file_hash.hexdigest()

"""
->Check that user provides correct command
->Get the source folder, replica folder, interval, and log file path from the command line arguments
"""

if __name__ == "__main__":
  if len(sys.argv) != 5:
    print("Usage: python3 folder_sync.py <source_folder> <replica_folder> <interval> <log_file>")
    sys.exit(1)

  source_folder = sys.argv[1]
  replica_folder = sys.argv[2]
  interval = int(sys.argv[3])
  log_file = sys.argv[4]

  sync_folders(source_folder, replica_folder, interval, log_file)