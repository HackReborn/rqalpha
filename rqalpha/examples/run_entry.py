from rqalpha.api import *
from rqalpha import run_file

sl = ['510050.XSHG', '510500.XSHG', '162411.XSHE']

config = {
    "base": {
        "start_date": "2015-08-19",
        "end_date": "2017-07-07",
        "benchmark": sl[0],
        "accounts": {
            "stock": 200000
        }
    },
    "mod": {
        "sys_simulation": {
            "enabled": True,
            "signal": True,
        },
        "sys_analyser": {
            "enabled": True,
            "plot": True,
        }
    }
}

str_format = lambda val: ('%.3f' % val).ljust(5)

strategy_file_path = "./mg_enhance_value.py"

result_dict = run_file(strategy_file_path, config)
summary = (result_dict['sys_analyser'])['summary']

logger.info("Result: alpha {}, beta {}, sharpe {}, information_ratio {}, total_returns {}"
            .format(str_format(summary['alpha']), str_format(summary['beta']),
                    str_format(summary['sharpe']), str_format(summary['information_ratio']),
                    str_format(summary['total_returns'])))


