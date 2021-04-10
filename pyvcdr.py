
class Signal(object):
    def __init__(self, var_type, size, reference, module):
        self.type = var_type
        self.size = size
        self.reference = reference
        self.module = module
        self.steps = []
        self.EMPTY_TIME=-1.23456789
        self.max_time = self.EMPTY_TIME
        self.min_time=self.EMPTY_TIME

    def step(self, time, value):
        self.steps.append((time, value))
        if self.max_time==self.EMPTY_TIME:
            self.max_time = int(time)
            self.min_time = int(time)
        else:
            ct = int(time)
            if(ct<self.min_time):
                self.min_time = ct
            if(ct>self.max_time):
                self.max_time = ct
    def __str__(self):
        return "Signal(%s, %s, %s, %s)" % (self.type, self.size, self.reference, self.module)


class VcdR(object):
    def __init__(self):
        self.EMPTY_TIME=-1.23456789
        self.signals=[]
        self.sig_dict = {}
        self.max_time = self.EMPTY_TIME
        self.min_time=self.EMPTY_TIME
        self.timescale = ''
        self.file_date = ""
        self.time_values=[]
        self.need_time_values = 1


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
            cmd_line.replace('$date','')
            cmd_line.replace('$end', '') #date must end with one line
            cmd_line = cmd_line.strip()
            self.file_date = cmd_line
        elif cmd == 'version':
            cmd_line.replace('$version','')
            cmd_line.replace('$end', '') #date must end with one line
            cmd_line = cmd_line.strip()
            self.file_date = cmd_line
        elif cmd == "comment":
            pass
        elif cmd == "end":
            pass
        elif cmd == "timescale":
            cmd_line.replace('$timescale','')
            cmd_line.replace('$end', '') #date must end with one line
            cmd_line = cmd_line.strip()
            self.timescale = cmd_line
        elif cmd == 'scope':
            pass
        elif cmd == 'var':
            var_line = cmd_line.split(' ');
            sig1 = Signal(var_line[1], var_line[2], var_line[3], var_line[4])
            self.signals.append(sig1)
            self.sig_dict[var_line[3]] = sig1
        elif cmd == 'upscope':
            pass
        elif cmd == 'enddefinitions':
            pass

    def process_time_value(self, time_value_line):
        time_v = time_value_line.split(' ')
        sig_cnt = len(time_v)-1
        time_val = int(time_v[0][1:])
        for i in time_v[1:]:
            i=i.strip()
            if i[-1] in self.sig_dict:
                self.sig_dict[ i[-1] ].step(time_val, i[0:-1])
                if self.need_time_values:
                    self.time_values.append((time_val, self.sig_dict[ i[-1] ].module, i[0:-1]))
            else:
                print('unknown id error???')
                print(i)






    def read_file(self, file_name):
        #read all file
        file1 = open(file_name)
        file_lines = file1.readlines()
        file1.close()
        # parse every line
        for i in file_lines:
            i.strip()
            if len(i) == 0:
                continue
            if i[0] == '#':
                self.process_time_value(i)
            elif i[0] == '$':
                #command?
                self.process_cmd(i)

        for i in self.signals:
            if self.min_time == self.EMPTY_TIME:
                self.min_time = i.min_time
                self.max_time = i.max_time
            else:
                if self.min_time>i.min_time:
                    self.min_time = i.min_time
                if self.max_time<i.max_time:
                    self.max_time = i.max_time


if __name__=="__main__":
    a = VcdR()
    a.read_file('./test1.vcd')
    print(a.signals[0])#Signal(wire, 1, !, D0)
    print(a.signals[1])#Signal(wire, 1, ", D1)
    print(a.signals[2])#Signal(wire, 1, #, D2)
    print(a.signals[1].module)#D1
    for i in a.signals[1].steps:
        print(i)
        #(0, '1') time, val
        #(1250, '0')
        #(6250, '1')
        #。。。
    for i in a.time_values:
        print('time:', i[0], '. sig:', i[1], '. val:', i[2])
        #(0, 'D0', '0')
        #(0, 'D1', '1')
        #(0, 'D2', '1')
        #(1250, 'D1', '0')
        #(6250, 'D1', '1')
        #(10000, 'D1', '0')
        #(15000, 'D1', '1')
        #...