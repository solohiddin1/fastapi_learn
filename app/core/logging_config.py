import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import date

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


handler = TimedRotatingFileHandler(
    filename=f"{LOG_DIR}/app_{date.today()}.log",
    when="midnight",
    interval=1,
    backupCount=10,
    encoding="utf-8"
)

handler.suffix = "%Y-%m-%d"  # optional: filename will include date

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)
# logging.basicConfig(
#     handlers=[
#         handler
#     ],
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
#     level=logging.INFO,
# )
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
# handler.doRollover()