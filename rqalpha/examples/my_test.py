from rqalpha.api import *


def init(context):
    context.s1 = "510500.XSHG"
    context.unit = 5000
    context.margin = 0.02
    context.lastp = 0
    context.no_cash_to_buy_total = 0
    context.no_share_to_sell_total = 0
    context.no_cash_to_buy = 0
    context.no_share_to_sell = 0
    context.inited = False
    logger.info("RunInfo: {}".format(context.run_info))


def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    bar = bar_dict[context.s1]
    if context.inited is False:
        context.inited = True
        order_value(context.s1, context.unit, price=bar.open)
        context.lastp = bar.open
        logger.info("Make first fire!")

    if bar.low < (context.lastp * (1-context.margin)) < bar.high:
        if context.portfolio.cash > context.unit:
            context.no_cash_to_buy = 0
            context.lastp *= (1 - context.margin)
            logger.info("order_value: low {}, p {}, high {}".format(bar.low, context.lastp, bar.high))
            order_value(context.s1, context.unit, price=context.lastp)
        else:
            context.no_cash_to_buy_total += 1
            context.no_cash_to_buy += 1
            logger.info("No cash to buy: {}".format(context.no_cash_to_buy_total))
            logger.info("Low spread: {}".format(1-(bar.low/context.lastp)))

    if bar.low <= (context.lastp * (1+context.margin)) <= bar.high:
        if context.portfolio.market_value > context.unit:
            context.no_share_to_sell = 0
            context.lastp *= (1 + context.margin)
            logger.info("order_value: low {}, p {}, high {}".format(bar.low, context.lastp, bar.high))
            order_value(context.s1, -1 * context.unit, price=context.lastp)
        else:
            context.no_share_to_sell_total += 1
            context.no_share_to_sell += 1
            logger.info("No share to sell: {}".format(context.no_share_to_sell_total))
            logger.info("High spread: {}".format((bar.high/context.lastp)-1))


def after_trading(context):
    pass