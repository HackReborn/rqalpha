def most_cash_prep(one_slot_size, start_p, wor_p, gap, lot_enhance):
    """
    :param one_slot_size:
    :param start_p:
    :param wor_p:
    :param gap: in percent, 0.05 means gap is 5% in strategy
    :param lot_enhance: in percent, 0.3 means 1.3 in strategy
    :return:
    """
    grids = round(((start_p - wor_p) / start_p) / gap)
    most = 0
    for gid in range(0, grids + 1):
        current_lot = round(one_slot_size * ((1 + lot_enhance) ** gid), 3)
        most += current_lot
        print("Gid ", gid,
              ": price %.3f" % (start_p * (1 - gap * gid)),
              ", lot %.3f" % current_lot, ", whole lot %.3f" % most)
    return most


# 500ETF 2018.07.18
print('500ETF')
most_cash_prep(one_slot_size=1, start_p=5.475, wor_p=4.884, gap=0.02, lot_enhance=0.4)

print('--------------------------------')

# HuaBao 2018.07.18
print('HuaBao')
most_cash_prep(one_slot_size=1, start_p=0.694, wor_p=0.5, gap=0.05, lot_enhance=0.3)
