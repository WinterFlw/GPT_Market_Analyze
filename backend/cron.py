import schedule
import time
from process_data import make_report_proto


def daily():
    make_report_proto(0)


def weekly():
    make_report_proto(1)


schedule.every().tuesday.at("05:01").do(daily())
schedule.every().wednesday.at("05:01").do(daily())
schedule.every().thursday.at("05:01").do(daily())
schedule.every().friday.at("05:01").do(daily())
schedule.every().saturday.at("05:01").do(daily())

schedule.every().tuesday.at("05:30").do(daily())
schedule.every().wednesday.at("05:30").do(daily())
schedule.every().thursday.at("05:30").do(daily())
schedule.every().friday.at("05:30").do(daily())
schedule.every().saturday.at("05:30").do(daily())


while True:
    schedule.run_pending()
    time.sleep(1)
