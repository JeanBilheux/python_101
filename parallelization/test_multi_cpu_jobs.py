import os
from concurrent.futures import ProcessPoolExecutor
from time import sleep
import platform

def worker(job, job_id):
    print(f"Job {job_id} running {job}")
    # execute the job
    # os.system(job)

    # get current cpu number used    
    os.system("top -b -n 1 | grep Cpu")

    print(f"{platform.processor() =}")
    
if __name__ == "__main__":
    num_jobs = 20
    list_jobs = ['ls', 'ls -l', 'ls -la', 'ls -lah', 'ls -lahR']
    with ProcessPoolExecutor(max_workers=num_jobs) as executor:
        executor.map(worker, list_jobs, range(num_jobs))