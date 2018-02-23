#
# Copyright (c) 2018, Carnegie Mellon University.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import sys
from docopt import docopt


class OptionParser:
    def __init__(self):
        self.__doc__ = """Overview:
        Parameter Generator

        Usage:
        random_execute.py [-c <D>] [-d <D>] [-f <D>] [-i <D>] [-m <D>] 
               [-o <NAME>] [-q <D>] [-s <D>] [-w <D>]
               [--server <IP_ADDRESS>] [--port <PORT>]
               [--database <NAME>] [--collection <NAME>]
               [--no-run <True/False>] [--tracer <True/False>]

        Options:
        -c <D> : Number of collections (default is Random)
        -d <D> : Number of documents (default is 10000)
        -f <D> : Number of fields (default is 5)
        -i <D> : Number of index patterns (default is 10)
        -m <D> : Number of fields in output format (default is 10)
        -o <NAME> : Output Filename (default is data.csv)
        -q <D> : Number of queries (default is 10000)
        -s <D> : Number of structure patterns (default is 10)
        -w <D> : Number of workload pattern (default is 100)
        --server <IP_ADDRESS> : client (default is 127.0.0.1)
        --port <PORT> : port (default is 27017)
        --database <NAME> : database name (default is testdb)
        --no-run <D>: True/False means run on mongodb or not(default is False)
        --tracer <D> : True/False means using tracer or not(experimental use)
        """

    def exec(self):
        command2option = {
            "-c": "num_of_collections",
            "-d": "num_of_documents",
            "-f": "num_of_fields",
            "-i": "num_of_indexs",
            "-m": "num_of_fields_in_format",
            "-o": "filename",
            "-q": "num_of_queries",
            "-s": "num_of_structures",
            "-w": "num_of_workloads",
            "--server": "server",
            "--port": "port",
            "--database": "database",
            "--no-run": "norun",
            "--tracer": "tracer"
        }
        options = {
            "num_of_collections": None,
            "num_of_fields": 5,
            "num_of_documents": 10000,
            "num_of_indexs": 1,
            "num_of_fields_in_format": 10,
            "upper_insert_many": 1000,
            "num_of_queries": 10000,
            "num_of_structures": 1,
            "num_of_workloads": 1,
            "server": "127.0.0.1",
            "port": "27017",
            "database":  "testdb",
            "norun": False,
            "tracer": False,
            "filename": "data.csv",
            "outdir": "./data/"
        }
        number_keys = ["-c", "-d", "-f", "-m", "-s", "-w"]
        args = docopt(self.__doc__)
        for command, opt in command2option.items():
            if args[command] is not None:
                if command in number_keys:
                    options[opt] = int(args[command])
                else:
                    options[opt] = args[command]
        self.__error_checker(options)
        return options

    def __error_checker(self, options):
        if options["num_of_collections"] is not None:
            if options["num_of_fields"] < options["num_of_collections"]:
                code = 'num_of_collections(-c) must be < num_of_fields(-f)'
                sys.stderr.write(code)
