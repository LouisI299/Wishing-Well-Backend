from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_scheduler(app):
    from .streak_checks import check_user_streaks
    jobstores = {
        'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
    }
    
    scheduler = BackgroundScheduler(jobstores=jobstores)
    
    scheduler.add_job(
        func=check_user_streaks,
        trigger='interval',
        minutes=1,
        id='streak_check',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler