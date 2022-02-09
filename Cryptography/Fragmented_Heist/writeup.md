The first part is a very faulty Shamir Secret Sharing Scehme implementation.(Inspired by https://btcarmory.com/fragmented-backup-vuln/).<br/> We are given a fragment which gives us the coefficient of x<sup>1</sup>(a<sub>1</sub>) . We can find out coefficients of x<sup>2</sup>(a<sub>2</sub>=hashAF(a<sub>1</sub>)) and x<sup>3</sup>(a<sub>3</sub>=hashAF(a<sub>2</sub>)) using the way the coefficients were generated.<br /> We can find (a<sub>0</sub>=hashAF(secret)) by substituting the coefficients <br />
<br />
The second part is understanding the hash function used.<br  />
<br />
Note that converting hashAF(secret) to bytes gives us something starting with "p_ct". We can have a good degree of confidence that "(res+ (res > 600 )) & 2\*\*(600) -1" is just res itself when we apply hashAF(secret). That is we can recover secret from hashAF(secret) <br />

Now observe the hashAF function. what it does is break down the input into blocks of 64 bits(=8 bytes)(with or without a initial block of size <64 bits) and adds extra noise of 32 bits(=4 bytes)(CRC) in between the blocks <br />
So We strip off the noise in between to get the flag <br />

```python
from Crypto.Util.number import long_to_bytes, bytes_to_long
from zlib import crc32


def hashAF(x):
    res = []
    final = b""
    bytesAF = long_to_bytes(x)
    a = bytesAF[:len(bytesAF) % 8]
    res.append(a)
    res.append(long_to_bytes(crc32(a)))
    t = (len(bytesAF) // 8)
    bytesAF = bytesAF[len(bytesAF) % 8:]
    for i in range(t):
        a = bytesAF[i*8:(i+1)*8]
        res.append(a)
        res.append(long_to_bytes(crc32(a)))
    for i in res:
        final += i
    res = bytes_to_long(final)
    return (res + (res >> 600)) & 2**(600)-1


x = 2720495220767623469285353744013822381852003568708186036185616503729980637299872397663528775139327535373882372413441024067687853130042950311733094495718491989102461186253653660920574
P = 93327214260434303138080906179883696131283277062733597039773430143631378719403851851296505697016458801222349445773245718371527858795457860775687842513513120173676986599209741174960099561600915819416543039173509037555167973076303047419790245327596338909743308199889740594091849756693219926218111062780849456373
y = 15843669386575231305658351759203181197336939290074172277291278488719033553337092007099376279196087414169431058207783322243407822366880172512356717418627958539974211317395928935201076097698103133753750610845316760255658006438109555979823148869170489527876600496043886788103609669557918594073292264548123406903
a = [0, x, hashAF(x), hashAF(hashAF(x))]
a[0] = y - (a[1] * x + a[2] * x**2 + a[3] * x**3) % P
ct = a[0]
ct = long_to_bytes(ct)
BLOCK = 8  # size of a text block in bytes
CRC = 4  # size of CRC in bytes
if len(ct) % (BLOCK+CRC) != 0:  # There is a residual block after splitting into blocks of 8+4 bytes(A Full text block +A CRC block)
    first = (len(ct) % (BLOCK+CRC))-CRC
    a = ct[:first]
    i = first+CRC
else:
    i = 0
while i < len(ct):
    a += ct[i:i+BLOCK]
    i += BLOCK+CRC
print(a.decode())
```
