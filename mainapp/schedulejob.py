# from apscheduler.schedulers.background import BackgroundScheduler
# from mainapp.models import Referral
# from deposit.models import InvestmentRequest
#
# # -------------------------------
# #                                |
# #           Django Schedule Job
# #                                |
# # -------------------------------
#
#
# def schedule_job():
#     print("--------------Schedule Job Started--------------------------")
#     print("* ROI Profit *")
#     print("* Sell Volume *")
#
#
# scheduler = BackgroundScheduler()
# job = None
#
#
# def start_job():
#     global job
#     job = scheduler.add_job(schedule_job, 'interval', seconds=10)
#     try:
#         scheduler.start()
#     except:
#         pass
#
#
# start_job()