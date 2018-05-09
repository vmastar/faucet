#!/usr/bin/env python

"""Standalone script to check FAUCET configuration, return 0 if provided config OK."""

# Copyright (C) 2015 Brad Cowie, Christopher Lorier and Joe Stringer.
# Copyright (C) 2015 Research and Education Advanced Network New Zealand Ltd.
# Copyright (C) 2015--2017 The Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

from faucet import valve
from faucet.config_parser import dp_parser
from faucet.conf import InvalidConfigError


def check_config(conf_files, debug_level):
    """Return True and successful config dict, if all config can be parsed."""
    logname = '/dev/null'
    logger = logging.getLogger('%s.config' % logname)
    logger_handler = logging.StreamHandler(stream=sys.stderr)
    logger.addHandler(logger_handler)
    logger.propagate = 0
    logger.setLevel(debug_level)
    check_output = ''
    check_result = False

    for conf_file in conf_files:
        try:
            _, dps = dp_parser(conf_file, logname)
            for dp in dps:
                valve_dp = valve.valve_factory(dp)
                if valve_dp is None:
                    check_result = False
                    break
                check_output = dp.to_conf()
                check_result = True
        except InvalidConfigError as config_err:
            check_output = config_err
    return (check_result, check_output)


def main():
    check_result, check_output = check_config(sys.argv[1:], logging.DEBUG)
    print(check_output)
    sys.exit(not check_result)


if __name__ == '__main__':
    main()
