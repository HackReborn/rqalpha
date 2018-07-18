from rqalpha.api import *
from rqalpha import run_file

sl = ['510500.XSHG', '162411.XSHE']

config = {
    "base": {
        "start_date": "2015-07-10",
        "end_date": "2018-07-05",
        "benchmark": sl[1],
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

#strategy_file_path = "./mg_same_value.py"
strategy_file_path = "./mg_enhance_value.py"

result_dict = run_file(strategy_file_path, config)
res_keys = result_dict['sys_analyser'].keys()
#for key in res_keys:
#    logger.info("------ {}: {}".format(key, (result_dict['sys_analyser'])[key]))


logger.info("------ {}:\n {}".format('trades', (result_dict['sys_analyser'])['trades']))


#logger.info("Result: {}".format(result_dict['sys_analyser'].keys()))
