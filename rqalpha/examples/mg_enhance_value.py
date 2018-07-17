from rqalpha.api import *


def init(context):
    context.S1 = "162411.XSHE"  # ""510500.XSHG"
    context.V_ENHANCE = 0.3
    context.UNIT = 11000
    context.INIT_S = 1
    context.MARGIN = 0.05
    context.FIRST_P = 0
    context.hold_level = -1
    context.hold_level_pre = 0
    context.inited = False
    logger.info("RunInfo: {}".format(context.run_info))


def before_trading(context):
    context.hold_level_pre = context.hold_level
    pass


def get_p_v(context, level):
    p = context.FIRST_P - ((level * context.MARGIN) * context.FIRST_P)
    if level >= 0:
        v = context.UNIT * ((1 + context.V_ENHANCE) ** level)
    else:
        v = context.UNIT * ((1 - context.V_ENHANCE) ** (-1 * level))
    return {'price': p, 'value': v}


def next_buy_p_v(context):
    return get_p_v(context, context.hold_level + 1)


def next_sell_p_v(context):
    # return get_p_v(context, context.hold_level-1)
    pv_sell = get_p_v(context, context.hold_level - 1)
    pv_curr = get_p_v(context, context.hold_level)
    return {'price': pv_sell['price'], 'value': pv_curr['value']}


def buy(context, bp):
    logger.info("buy: {}".format(bp))
    if context.portfolio.cash < bp['value']:
        logger.warn("Failed buy: price {}, need_cash {}, remain_cash {}"
                    .format(bp['price'], bp['value'], context.portfolio.cash))
        return
    res = order_value(context.S1, bp['value'], price=bp['price'])
    if res.status == ORDER_STATUS.FILLED:
        context.hold_level += 1
        logger.info("Hold level changed: {}".format(context.hold_level))
    else:
        logger.warn("Failed buy: {}".format(res))


def sell(context, sp):
    logger.info("sell: {}".format(sp))
    if context.portfolio.market_value < sp['value']:
        logger.warn("Failed sell: price {}, need_value {}, remain_value {}"
                    .format(sp['price'], sp['value'], context.portfolio.market_value))
        return
    res = order_value(context.S1, -1 * sp['value'], price=sp['price'])
    if res.status == ORDER_STATUS.FILLED:
        context.hold_level -= 1
        logger.info("Hold level changed: {}".format(context.hold_level))
    else:
        logger.warn("Failed sell: {}".format(res))


def handle_bar(context, bar_dict):
    bar = bar_dict[context.S1]
    if context.inited is True:
        nextBp = next_buy_p_v(context)
        nextSp = next_sell_p_v(context)
    if context.inited is False:
        context.inited = True
        context.FIRST_P = bar.close
        buy(context, {'price': context.FIRST_P, 'value': context.UNIT * context.INIT_S})

    elif bar.low <= nextBp['price'] <= bar.high:
        buy(context, nextBp)

    elif bar.high < nextBp['price']:
        buy(context, {'price': bar.high, 'value': nextBp['value']})

    elif bar.low <= nextSp['price'] <= bar.high:
        sell(context, nextSp)

    elif bar.low > nextSp['price']:
        sell(context, {'price': bar.low, 'value': nextSp['value']})


def after_trading(context):
    if context.hold_level_pre != context.hold_level:
        profit = (context.portfolio.cash + context.portfolio.market_value - context.portfolio.starting_cash)
        logger.info("after_trading: market_value {}, profit {}, profit-pct {}".
                    format(context.portfolio.market_value, profit, profit/context.portfolio.market_value))
        # profit_pct = profit / (context.portfolio.market_value - profit)
        # logger.info("after_trading: market_value {}, profit {}, percent {}".
        #             format(context.portfolio.market_value, profit, profit_pct))
