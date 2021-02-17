#! /usr/bin/python3

from bin.logger import Logger
from bin.report import Report
import setup.config as cfg
from datetime import datetime, date, timedelta
import sys,getopt

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hmdw",["help","day","month"])
    except getopt.GetoptError:
        print('Wrong option! Try to use -h to get help.')
        sys.exit(2)
    if opts == None:
        print('Please use -d -w or -m')
        exit(-1)
    log = Logger(cfg.path_to_log_file)
    date = datetime.now()
    today_stamp = datetime.timestamp(date)
    opts = opts[0]
    opts = opts[0]
    if opts in ('-d','--day'):
        from_stamp = datetime.timestamp(date - timedelta(hours=24))
    elif opts in ('-m','--month'):
        from_stamp = datetime.timestamp(datetime.today() - timedelta(days=31))
    elif opts in ('-w','--week'):
        from_stamp = datetime.timestamp(datetime.today() - timedelta(days=7))
    report = Report(log, from_stamp, today_stamp)
    report.get_data()
    report.gen_report()
    report.send_report()

if __name__=="__main__":
    main(sys.argv[1:])
