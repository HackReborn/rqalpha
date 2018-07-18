from rqalpha.api import *

sl = ['510500.XSHG', '162411.XSHE']
gl = [0.02, 0.05]
lot_l = [10000, 7000]
en_l = [0.4, 0.4]


p_format = lambda val: ('%.3f' % val).ljust(10)
lot_format = lambda val: ('%.0f' % val).ljust(10)


def init(context):
    context.S1 = sl[1]
    context.V_ENHANCE = en_l[1]
    context.UNIT = lot_l[1]
    context.INIT_S = 1
    context.MARGIN = gl[1]
    context.FIRST_P = 0
    context.hold_level = -1
    context.inited = False
    logger.info("RunInfo: {}".format(context.run_info))


def before_trading(context):
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
    if context.portfolio.cash < bp['value']:
        logger.warn("Fail to buy".ljust(10) + ':' + trade_info(context, bp))
        return
    res = order_value(context.S1, bp['value'], price=bp['price'])
    if res.status == ORDER_STATUS.FILLED:
        context.hold_level += 1
        logger.info("Buy".ljust(10) + ':' + trade_info(context, bp))
    else:
        logger.warn("Failed buy: {}".format(res))


def sell(context, sp):
    if context.portfolio.market_value < sp['value']:
        logger.warn("Fail to sell".ljust(10) + ':' + trade_info(context, sp))
        return
    res = order_value(context.S1, -1 * sp['value'], price=sp['price'])
    if res.status == ORDER_STATUS.FILLED:
        context.hold_level -= 1
        logger.info("Sell".ljust(10) + ':' + trade_info(context, sp))
    else:
        logger.warn("Failed sell: {}".format(res))


def trade_info(context, tp):
    return "gid {} price {} lot {} sum_lot {} cash {} profit {}"\
        .format(lot_format(context.hold_level),
                p_format(tp['price']),
                lot_format(tp['value']),
                lot_format(context.portfolio.market_value),
                lot_format(context.portfolio.cash),
                lot_format(context.portfolio.cash + context.portfolio.market_value - context.portfolio.starting_cash))


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
    pass
