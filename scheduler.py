import time
import subprocess

def run_cycle():
    print("🚀 Running SEO generation cycle...")

    subprocess.run(["python", "auto_generator.py"])

    print("✅ Cycle complete")

# -----------------------
# LOOP (every 6 hours)
# -----------------------
if __name__ == "__main__":

    while True:
        run_cycle()

        print("⏳ Sleeping for 6 hours...")
        time.sleep(6 * 60 * 60)
