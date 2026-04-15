import time
from datetime import datetime

from auto_generator import run as generate_pages
from indexer import run as register_pages
from optimizer import run as optimize_pages
from logger import log_cycle

# ----------------------------
# CONFIG
# ----------------------------
DAILY_PAGE_LIMIT = 100   # <-- THIS controls how many pages/day you generate
RUN_OPTIMIZER = True     # turn off if you want faster runs

# ----------------------------
# CYCLE START
# ----------------------------
def run_daily_cycle():

    log_cycle("START")

    print("===================================")
    print("🚀 SEO ENGINE DAILY CYCLE STARTED")
    print("===================================")
    print(f"⏰ Time: {datetime.now()}")
    print(f"📊 Daily Limit: {DAILY_PAGE_LIMIT}")
    print("")

    try:
        # ------------------------
        # 1. GENERATE PAGES
        # ------------------------
        print("🟢 Step 1: Generating pages...")
        generate_pages(limit=DAILY_PAGE_LIMIT)

        # ------------------------
        # 2. REGISTER PAGES
        # ------------------------
        print("🔵 Step 2: Registering pages...")
        register_pages()

        # ------------------------
        # 3. OPTIMIZE (optional)
        # ------------------------
        if RUN_OPTIMIZER:
            print("🟣 Step 3: Optimizing pages...")
            optimize_pages()

        print("")
        print("✅ DAILY CYCLE COMPLETED SUCCESSFULLY")

        log_cycle("END_SUCCESS")

    except Exception as e:

        print("❌ ERROR IN DAILY CYCLE:", str(e))
        log_cycle(f"ERROR: {str(e)}")


# ----------------------------
# MAIN ENTRY
# ----------------------------
if __name__ == "__main__":

    run_daily_cycle()
