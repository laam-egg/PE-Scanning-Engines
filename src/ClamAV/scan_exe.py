# Python 3.12

import os
import subprocess
import time

def is_exe_file(filename):
    return filename.lower().endswith('.exe')

def run_clamdscan(filepath):
    try:
        start_time = time.perf_counter()
        result = subprocess.run(
            ['clamdscan', '--no-summary', '--fdpass', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        output = result.stdout.strip()
        if ':' in output:
            scanned_path, status = output.split(':', 1)
            status = status.strip()
            return status, output, duration
        else:
            return 'ERROR', output, duration
    except Exception as e:
        return f'ERROR', str(e), 0

def scan_directory(root_dir):
    total = 0
    infected = 0
    errors = 0
    total_duration = 0

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if is_exe_file(fname):
                full_path = os.path.join(dirpath, fname)
                print(f"Inspecting {full_path} ... ", end="", flush=True)
                status, output, duration = run_clamdscan(full_path)
                total += 1
                total_duration += duration

                if status == 'OK':
                    print(f"BENIGN ", end=" | ", flush=True)
                    print(f"{duration:.2f} s")
                elif status == 'ERROR':
                    errors += 1
                    print(f"ERROR  ", end=" | ", flush=True)
                    print(f"{duration:.2f} s")
                    print("                                         ", status)
                else:
                    infected += 1
                    print(f"MALWARE", end=" | ", flush=True)
                    print(f"{duration:.2f} s")
                    print("                                         ", status)

    print('\n===== Scan Summary =====')
    print(f'Total .exe files scanned: {total}')
    print(f'Infected files: {infected}')
    print(f'Errors: {errors}')
    print(f'Total inference time: {total_duration:.3f} s')
    print()
    print(f"Infected percentage: {(infected / total * 100):.2f}%")
    print(f"Error percentage: {(errors / total * 100):.2f}%")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} /path/to/scan')
        exit(1)
    scan_directory(sys.argv[1])
