from rqalpha.api import *


def init(context):
    context.s1 = "000001.XSHE"
    logger.info("RunInfo: {}".format(context.run_info))


def before_trading(context):
    logger.info("+++++ Run in before_trading +++++")


def handle_bar(context, bar_dict):
    logger.info("in handle bar")
    logger.info("print bar data:")
    logger.info(bar_dict[context.s1])


def after_trading(context):
    logger.info("----- after_trading ------")
