import yaml
import logging.config
import logging

with open('./config/logging.yaml', 'r+') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('temperature-monitoring-bot')
logging.getLogger("apscheduler.executors.default").setLevel(logging.CRITICAL)
