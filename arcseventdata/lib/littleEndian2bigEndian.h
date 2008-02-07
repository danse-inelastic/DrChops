/// copied from http://www.devx.com/tips/Tip/34353?trk=DXRSS_JAVA

// 2-byte number
inline int SHORT_little_endian_TO_big_endian(int i)
{
    return ((i>>8)&0xff)+((i << 8)&0xff00);
}

// 4-byte number
inline int INT_little_endian_TO_big_endian(int i)
{
    return((i&0xff)<<24)+((i&0xff00)<<8)+((i&0xff0000)>>8)+((i>>24)&0xff);
}

