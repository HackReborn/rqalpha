from rqalpha.api import *
from rqalpha import run_file

config = {
    "base": {
        "start_date": "2017-03-01",
        "end_date": "2018-07-01",
        "benchmark": '162411.XSHE',
        "accounts": {
            "stock": 100000
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

#logger.info("Result: {}".format(result_dict))
