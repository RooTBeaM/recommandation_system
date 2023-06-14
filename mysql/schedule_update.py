import schedule
import time
from main import mode_0,mode_1,mode_4
print(f'schedule process every 5 minutes was started.')
start = time.time()
def job():
    mode_0()
    mode_1()
    mode_4()
    print(f'schedule process every 5 minutes was started.')
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

# mode_0()
# mode_1()
# mode_4()