import schedule
import time
import subprocess
import datetime


def retrain_model_m1():
    date = datetime.date.today()

    subprocess.run(["bash", "ml/svd.sh", str(date), "1"])
    print("Retraining model 1", date)


def retrain_model_m2():
    date = datetime.date.today()

    subprocess.run(["bash", "ml/svd.sh", str(date), "2"])
    print("Retraining model 2", date)


# schedule.every(3).days.do(retrain_model_m1)
# schedule.every(3).days.do(retrain_model_m2)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
retrain_model_m1()
retrain_model_m2()
