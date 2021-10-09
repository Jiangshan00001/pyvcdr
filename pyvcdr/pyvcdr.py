# coding=utf-8

class Signal(object):
    def __init__(self, var_type, size, reference, module):
        self.type = var_type
        self.size = size
        self.reference = reference
        self.module = module
        self.steps = []
        self.EMPTY_TIME = -1.23456789
        self.max_time = self.EMPTY_TIME
        self.min_time = self.EMPTY_TIME

    def step(self, time, value):
        self.steps.append((time, value))
        if self.max_time == self.EMPTY_TIME:
            self.max_time = int(time)
            self.min_time = int(time)
        else:
            ct = int(time)
            if(ct < self.min_time):
                self.min_time = ct
            if(ct > self.max_time):
                self.max_time = ct

    def __str__(self):
        return "Signal(%s, %s, %s, %s)" % (self.type, self.size, self.reference, self.module)


class VcdR(object):

    def __init__(self):
        self.EMPTY_TIME = -1.23456789
        self.signals = []
        self.sig_dict = {}
        self.max_time = self.EMPTY_TIME
        self.min_time = self.EMPTY_TIME
        self.timescale = ''
        self.file_date = ""
        self.time_values = []
        self.need_time_values = 1
        # after $enddefinitions $end command. all data is:# time value etc...
        self.m_is_definition_end = 0
        self.parsed_curr_time = 0
        self.curr_cmd = ''
        self.curr_line = 0

    def process_cmd(self, cmd_line):
        # find sapce or end
        space_index = cmd_line.find(' ')
        if space_index == -1:
            space_index = cmd_line.find('\n')
        if space_index == -1:
            space_index = cmd_line.find('\r')

        cmd = cmd_line[1:space_index]
        cmd.strip()
        if cmd == "date":
            cmd_line.replace('$date', '')
            cmd_line.replace('$end', '')  # date must end with one line
            cmd_line = cmd_line.strip()
            self.file_date = cmd_line
        elif cmd == 'version':
            cmd_line.replace('$version', '')
            cmd_line.replace('$end', '')  # date must end with one line
            cmd_line = cmd_line.strip()
            self.file_date = cmd_line
        elif cmd == "comment":
            self.curr_cmd = cmd
            pass
        elif cmd == "end":
            self.curr_cmd = ''
            pass
        elif cmd == "timescale":
            cmd_line.replace('$timescale', '')
            cmd_line.replace('$end', '')  # date must end with one line
            cmd_line = cmd_line.strip()
            self.timescale = cmd_line
        elif cmd == 'scope':
            pass
        elif cmd == 'var':
            var_line = cmd_line.split(' ')
            sig1 = Signal(var_line[1], var_line[2], var_line[3], var_line[4])
            self.signals.append(sig1)
            self.sig_dict[var_line[3]] = sig1
        elif cmd == 'upscope':
            pass
        elif cmd == 'enddefinitions':
            self.m_is_definition_end = 1
        elif cmd == 'dumpvars':
            pass
        else:
            print('unknown cmd. may be an error:', cmd)

    def parse_elem_list(self, time_val, elem_list):
        while '' in elem_list:
            elem_list.remove('')

        if len(elem_list) == 0:
            return
        elif elem_list[0][0] in 'BbRr':
            # two elem needed for one
            sig_val = elem_list[0]
            sig_var = elem_list[1]
            self.add_one_sig(time_val, sig_val, sig_var)
            self.parse_elem_list(time_val, elem_list[2:])
        elif elem_list[0][0] in '01':
            # one elem for one
            if len(elem_list[0]) > 1:
                sig_val = elem_list[0][0]
                sig_var = elem_list[0][1:]
                self.add_one_sig(time_val, sig_val, sig_var)
                self.parse_elem_list(time_val, elem_list[1:])
            else:
                sig_val = elem_list[0]
                sig_var = elem_list[1]
                self.add_one_sig(time_val, sig_val, sig_var)
                self.parse_elem_list(time_val, elem_list[2:])
        else:
            print('unsupported elem。 line=', self.curr_line, time_val, elem_list)

    def process_time_value(self, time_value_line):
        time_value_line = time_value_line.strip()
        time_v = time_value_line.split(' ')
        time_val = int(time_v[0][1:])
        self.parsed_curr_time = time_val
        self.parse_elem_list(self.parsed_curr_time, time_v[1:])

    def add_one_sig(self, ctime, cval, csig):
        if csig in self.sig_dict:
            self.sig_dict[csig].step(ctime, cval)
            if self.need_time_values:
                self.time_values.append((ctime, self.sig_dict[csig].module, cval))
        else:
            print('unknown id error. line=', self.curr_line, ctime, cval, csig)

    def process_with_last_cmd(self, curr_content):
        if self.curr_cmd == 'comment':
            # in comment. just skip
            return
        if not self.m_is_definition_end:
            print('WARNING: i could not parse the line:', self.curr_line, curr_content)
            print('just skip the line')
            return
        curr_content = curr_content.strip()
        if len(curr_content) == 0:
            return
        value_vs_sig = curr_content.split(' ')
        self.parse_elem_list(self.parsed_curr_time, value_vs_sig)

    def parse_str(self, vcd_str):
        # read all str
        file_lines = vcd_str.split('\n')

        self.curr_line = 0
        # parse every line
        for i in file_lines:
            self.curr_line = self.curr_line + 1
            i.strip()
            if len(i) == 0:
                continue
            if i[0] == '#':
                self.process_time_value(i)
            elif i[0] == '$':
                # command?
                self.process_cmd(i)
            else:
                self.process_with_last_cmd(i)

        # calc max min time
        for i in self.signals:
            if self.min_time == self.EMPTY_TIME:
                self.min_time = i.min_time
                self.max_time = i.max_time
            else:
                if self.min_time > i.min_time:
                    self.min_time = i.min_time
                if self.max_time < i.max_time:
                    self.max_time = i.max_time

    def read_file(self, file_name):
        # read all file
        file1 = open(file_name)
        file_lines = file1.read()
        file1.close()
        self.parse_str(file_lines)


def test1_vcd_parse():
    a = VcdR()
    a.read_file('./test1.vcd')
    print(a.signals[0])  # Signal(wire, 1, !, D0)
    print(a.signals[1])  # Signal(wire, 1, ", D1)
    print(a.signals[2])  # Signal(wire, 1, #, D2)
    print(a.signals[1].module)  # D1
    for i in a.signals[1].steps:
        print(i)
        # (0, '1') time, val
        # (1250, '0')
        # (6250, '1')
        # ...
    for i in a.time_values:
        print('time:', i[0], '. sig:', i[1], '. val:', i[2])
        # (0, 'D0', '0')
        # (0, 'D1', '1')
        # (0, 'D2', '1')
        # (1250, 'D1', '0')
        # (6250, 'D1', '1')
        # (10000, 'D1', '0')
        # (15000, 'D1', '1')
        # ...


def test2_vcd_parse():
    a = VcdR()
    a.read_file('./test2.vcd')
    print(a.signals[0])  # Signal(wire, 1, !, D0)
    print(a.signals[1])  # Signal(wire, 1, ", D1)
    print(a.signals[2])  # Signal(wire, 1, #, D2)
    print(a.signals[1].module)  # D1
    for i in a.signals[1].steps:
        print(i)
        # (0, '1') time, val
        # (1250, '0')
        # (6250, '1')
        # ...
    for i in a.time_values:
        print('time:', i[0], '. sig:', i[1], '. val:', i[2])
        # (0, 'D0', '0')
        # (0, 'D1', '1')
        # (0, 'D2', '1')
        # (1250, 'D1', '0')
        # (6250, 'D1', '1')
        # (10000, 'D1', '0')
        # (15000, 'D1', '1')
        # ...


def test3_vcd_parse():
    a = VcdR()
    a.read_file('./test3.vcd')
    print(a.signals[0])  # Signal(wire, 1, !, D0)
    print(a.signals[1])  # Signal(wire, 1, ", D1)
    print(a.signals[2])  # Signal(wire, 1, #, D2)
    print(a.signals[1].module)  # D1
    for i in a.signals[1].steps:
        print(i)

    for i in a.time_values:
        print('time:', i[0], '. sig:', i[1], '. val:', i[2])


if __name__ == "__main__":
    test3_vcd_parse()
    test2_vcd_parse()
    test1_vcd_parse()
