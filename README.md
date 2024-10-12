# sync_folders
Fulfilling the Requirements

One-way synchronization: The code ensures that only changes from the source folder are reflected in the replica folder.
Periodic synchronization: The script runs continuously, synchronizing the folders at a user-defined interval alhtough its in seconds it can be set to hours.
File Operations Logging: All file creation, copying, and removal actions are logged to a file and the console.
Command-Line Arguments: The script accepts command-line arguments for specifying folder paths, synchronization interval, and log file path.
Avoidance of third-party synchronization libraries: The synchronization logic is implemented from scratch, without relying on any external libraries. 
Use of external libraries for well-known algorithms: The hashlib library is used for calculating MD5 hashes, adhering to the recommendation to use existing libraries for common algorithms.
