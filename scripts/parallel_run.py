import subprocess
import time
from pathlib import Path

# Path to the MODFLOW executable and the main mfsim.nam file
modflow_executable = "/home/haqqanuddin/modflow6/bin/mf6"
mfsim_nam_path = Path("/home/haqqanuddin/mf6_quetta_splitted_2/mfsim.nam")

# Output file for logging times
log_file = Path("parallel_model_times.txt")

# Initialize log file with headers
with log_file.open("w") as log:
    log.write("Start Time, End Time, Elapsed Time (seconds), Status\n")

# Record start time
start_time = time.time()

# Start subprocess for model execution (main mfsim.nam file)
process = subprocess.Popen(
    ["mpirun", "-np", "4", modflow_executable, str(mfsim_nam_path)],  # Run with 4 processes (one for each part)
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=str(mfsim_nam_path.parent)  # Set working directory to where mfsim.nam is located
)

# Collect and log times for the model once completed
stdout, stderr = process.communicate()
end_time = time.time()
elapsed_time = end_time - start_time

# Log the results
with log_file.open("a") as log:
    if process.returncode == 0:
        end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
        log.write(f"{start_time}, {end_time_str}, {elapsed_time:.2f}, Completed\n")
        print(f"Main model (mfsim.nam) completed in {elapsed_time:.2f} seconds.")
    else:
        log.write(f"{start_time}, {elapsed_time:.2f}, Failed, Error: {stderr.decode()}\n")
        print(f"Main model (mfsim.nam) failed to run. Error: {stderr.decode()}")

print(f"Times logged to {log_file.resolve()}")
