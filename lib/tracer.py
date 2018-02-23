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

import subprocess
import time
import re
from subprocess import Popen


class Tracer:
    def __init__(self, qid, norun, tracer):
        self.norun = norun
        self.tracer = tracer
        self.qid = qid
        self.stat = "mongostat > ./log"
        replay = "~/mongo-tools/bin/mongoreplay"
        self.replay = "sudo " + replay + " record -p ./playback_tmp -i lo "
        self.replay_convert = replay + " monitor --collect json "
        self.replay_convert += " --report test.json -p ./playback_tmp"
        self.rm = "rm -f ./playback_tmp"

    def exec(self):
        if self.norun is False and self.tracer is True:
            self.kill()
            Popen(self.stat, shell=True)
            Popen(self.replay, shell=True)
            time.sleep(10)

    def convert(self):
        if self.norun is False and self.tracer is True:
            Popen(self.replay_convert, shell=True)

    def remove(self):
        if self.norun is False and self.tracer is True:
            Popen(self.rm, shell=True)

    def kill(self):
        if self.norun is False and self.tracer is True:
            for name in ["mongostat", "mongoreplay"]:
                pids = self.__get_pids(name)
                if len(pids) > 0:
                    tpids = " ".join(pids)
                    print(name, "KILLED", tpids)
                    Popen("sudo kill -SIGINT " + tpids, shell=True)

    def __get_pids(self, name):
        cmd = "ps aux | grep " + name + " | grep -v grep"
        proc = Popen(cmd, shell=True, stdout=subprocess.PIPE)
        target_pids = []
        while True:
            line = proc.stdout.readline()
            words = re.split(" +", str(line))
            if len(words) > 2:
                target_pids.append(words[1])
            if not line and proc.poll() is not None:
                break
        return target_pids
