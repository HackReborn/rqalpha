from rqalpha.api import *


class StratergyObj:
    def __init__(self, subj, lot, gap, enhance):
        self.subj = subj;
        self.lot = lot
        self.gap = gap;
        self.enhance = enhance

    def get_subj(self):
        return self.subj

    def get_gap(self):
        return self.gap

    def get_lot(self):
        return self.lot

    def get_enhance(self):
        return self.enhance

    def __str__(self):
        return "subj: " + self.subj + ", lot: " + str(self.lot) + ", gap: "\
               + str(self.gap) + ", enhance: " + str(self.enhance)


PRINT_ADJ = 15

CONFIG = {'510050.XSHG': StratergyObj(subj='510050.XSHG', lot=10000, gap=0.03, enhance=0.4),
          '510500.XSHG': StratergyObj(subj='510500.XSHG', lot=10000, gap=0.02, enhance=0.4),
          '162411.XSHE': StratergyObj(subj='162411.XSHE', lot=7000, gap=0.05, enhance=0.4),
          }


p_format = lambda val: ('%.3f' % val).ljust(10)
lot_format = lambda val: ('%.0f' % val).ljust(10)


def init(context):
    SUBJ = CONFIG['510050.XSHG']
    context.S1 = SUBJ.get_subj()
    context.LOT = SUBJ.get_lot()
    context.GAP = SUBJ.get_gap()
    context.ENHANCE = SUBJ.get_enhance()
    context.INIT_LOTS = 1
    context.START_PRICE = 0
    context.hold_level = -1
    context.inited = False
    #logger.info("RunInfo: {}".format(context.run_info))
    logger.info("-------------- " + SUBJ.__str__() + " --------------")


def before_trading(context):
    pass


def get_p_v(context, level):
    p = context.START_PRICE - ((level * context.GAP) * context.START_PRICE)
    if level >= 0:
        v = context.LOT * ((1 + context.ENHANCE) ** level)
    else:
        v = context.LOT * ((1 - context.ENHANCE) ** (-1 * level))
    return {'price': p, 'value': v}


def next_buy_p_v(context):
    return get_p_v(context, context.hold_level + 1)


def next_sell_p_v(context):
    # return get_p_v(context, context.hold_level-1)
    pv_sell = get_p_v(context, context.hold_level - 1)
    pv_curr = get_p_v(context, context.hold_level)
    return {'price': pv_sell['price'], 'value': pv_curr['value']}


def buy(context, bp):
    if bp['value'] < 0.5 * context.LOT:
        logger.warn("Ignore buy".ljust(PRINT_ADJ) + ':' + trade_info(context, bp))
        return
    if context.portfolio.cash < bp['value']:
        logger.warn("Fail to buy".ljust(PRINT_ADJ) + ':' + trade_info(context, bp))
        return
    res = order_value(context.S1, bp['value'], price=bp['price'])
    if res.status == ORDER_STATUS.FILLED:
        context.hold_level += 1
        logger.info("Buy".ljust(PRINT_ADJ) + ':' + trade_info(context, bp))
    else:
        logger.warn("Failed buy: {}".format(res))


def sell(context, sp):
    if sp['value'] < 0.5 * context.LOT:
        sp['value'] = 0.5 * context.LOT;
    if context.portfolio.market_value < sp['value']:
        logger.warn("Fail to sell".ljust(PRINT_ADJ) + ':' + trade_info(context, sp))
        return
    res = order_value(context.S1, -1 * sp['value'], price=sp['price'])
    if res.status == ORDER_STATUS.FILLED:
        context.hold_level -= 1
        logger.info("Sell".ljust(PRINT_ADJ) + ':' + trade_info(context, sp))
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
        context.START_PRICE = bar.close
        buy(context, {'price': context.START_PRICE, 'value': context.LOT * context.INIT_LOTS})

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
