import multiprocessing
import subprocess

def run_blender_instance(start, end, script_path):
    blender_command = [
        "blender",
        "--background",
        "--python", script_path,
        "--",
        f"--start={start}",
        f"--end={end}"
    ]
    print(f"Executing: {' '.join(blender_command)}")
    subprocess.run(blender_command, check=True)

def main():
    num_images = 11000
    num_processes = 12
    chunk_size = num_images // num_processes

    script_path = "synthetic_data_generation_4k.py"
    args = [
        (i * chunk_size, (i + 1) * chunk_size if i < num_processes - 1 else num_images, script_path)
        for i in range(num_processes)
    ]

    with multiprocessing.Pool(num_processes) as pool:
        pool.starmap(run_blender_instance, args)

if __name__ == "__main__":
    main()
