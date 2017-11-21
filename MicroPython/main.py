# system modules
import utime as time
import gc
# custom modules
from machine import UART
import esp

debugging = True


# generate random demo data

time.sleep(3)

deps = []

def randint(_range):
    return int.from_bytes(uos.urandom(1), 'little')/255*_range

def genrand(num, interval, variance):
    _deps = []
    for n in range(num):
        x = round(60*(n*interval+randint(variance)+randint(interval)+1))
        if x > 0 and x/60 < 100:
            _deps.append(x)
        else:
            print("whaaat {}".format(x))
            _deps.append(-999)
    return _deps

deps.extend(genrand(5, 5,4))
deps.extend(genrand(5, 5,4))
deps.extend(genrand(5, 7,5))
deps.extend(genrand(5, 7,5))
deps.extend(genrand(5, 7,5))
deps.extend(genrand(5, 7,5))
deps.extend(genrand(3, 20,2))
deps.extend([-999, -999])
deps.extend(genrand(3, 20,2))
deps.extend([-999, -999])

# Output data to Arduino
print("BEGIN SEND")
uart = UART(1,9600) # TX: GPIO2=D4, RX: none? (GPIO is also LED!)
time.sleep(0.1)
uart.write('{')
uart.write('\n')
for dep in deps:
    uart.write("{} \n".format(dep))
    time.sleep(0.01) # give Arduino time to read the buffer
uart.write("}")
uart.write('\n')
uart.write('\n')
print("END SEND")
print("")
for dep in deps:
    print     ("{}\t".format(dep), end="")
    # print     ("{:>4} \t".format(deps), end="")
    print("")
print("")

# no deep sleep for demo
