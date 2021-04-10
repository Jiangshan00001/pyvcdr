# pyvcdr
this is a python library for vcd wave file read.


readfile:
```
    a = VcdR()
    a.read_file('./test1.vcd')
```

after read. their are two ways to read the data.
first is read data by signal:
```	
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
```
second is read data by time:
```		
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
```		







