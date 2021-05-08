# pyvcdr
this is a python library for vcd wave file read.

# install:
```
pip install pyvcdr
```

or just copy pyvcdr.py file to your project.


# readfile:
```
    import pyvcdr
    a = pyvcdr.VcdR()
    a.read_file('./test1.vcd')
```

# use the data:

after read. their are two ways to access the data.
first is access data by signal:
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
second is access data by time:
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





# why I write this code:

I need a python vcd file read program.

I used this library first:
https://github.com/westerndigitalcorporation/pyvcd
but it could not read file. just write is supported.

then this one:
https://github.com/em-/python-vcd/tree/master/vcd
it works, but is very very slow.



# info and thanks:

the class Signal is from pyvcd library. 

# any issues：

I just write it for my file read. so it may not fit some IEEE 1364-2005 protocol.
if it do not work for you,
add an issue on github:
https://github.com/Jiangshan00001/pyvcdr

post the file that could not work.
or you can also change the code yourself.

CHANGE:
V0.6 2021.5.8. add suport for bBrR data support.




