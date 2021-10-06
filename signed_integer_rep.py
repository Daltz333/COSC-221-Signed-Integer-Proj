# Dalton Smith
# COSC 221
# 10/05/2021
# Inline functions are the devil

import math

def get_signed_mag_bin(bits: str):
    counter = 0
    signed_mag = 0
    sign = 0

    for bit in bits[::-1]:
        if (counter == 7):
            sign = int(bit)
            break
        if int(bit) == 0:
            pass # no need to process
        else:
            signed_mag += math.pow(2, counter)

        counter += 1
    
    return [sign, signed_mag]


def flip_str(bits: str):
    new_bits = ""
    for bit in bits:
        if int(bit) == 0:
            new_bits += "1"
        else:
            new_bits += "0"

    return new_bits
    

def handle_int(num: str):
    # See handle_binary for a bit of how this works
    # This function heavily uses inline functions
    # Basically, we just convert our base number to binary and do some math on that
    # zfill just ensures we always get an 8 bit number
    signed_mag = str(bin(int(num))).split("0b")[1].zfill(7)
    print("Signed Mag:", "1" + signed_mag.zfill(7) if int(num) < 0 else signed_mag.zfill(8))
    print("One's Comp:", "1" + flip_str(signed_mag).zfill(7) if int(num) < 0 else signed_mag.zfill(8))
    print("Two's Comp:", "1" + str(bin(int("0b" + flip_str(signed_mag), 2) + int("0b0000001", 2))).replace("0b", "").zfill(7) if int(num) < 0 else signed_mag.zfill(8))
    excess_128 = str(bin(int(signed_mag, 2) - 128)).replace("0b", "").zfill(8)
    print("Excess 128:", excess_128.replace("-","0"))


def handle_binary(num: str):
    # Process Signed Magnitude
    # Way harder than it was supposed to be, because Python delimits
    # integers that start with 0
    # Basically, the code splits it into "sign" and "bit values" and
    # handles logic based on that
    signed_mag = get_signed_mag_bin(num)
    print("Signed Mag:", signed_mag[1] if int(signed_mag[0]) == 0 else "-" + str(signed_mag[1]))

    signed_flip = get_signed_mag_bin(num[:1] + flip_str(num[-7:]))
    print("One's Comp:", "-" + str(signed_flip[1]) if int(signed_flip[0]) == 1 else str(signed_mag[1]))

    signed_flip_two = int("0b" + str(flip_str(num[-7:])), 2) + int("0b0000001", 2)
    print("Two's Comp:", "-" + str(signed_flip_two) if signed_flip[0] else str(signed_mag[1]))

    excess_128 = int(num, 2) - 128
    print("Excess 128:", excess_128)


# It's a little icky that we're using recursion of __main__()
# If the program was a bit bigger in scope, I'd create a state machine
# to handle looping through user queries. This is fine for a small project
def __main__():
    signed_int = False

    num = input("Enter signed integer (-128 to 127) or 8 bit binary: ")

    # Verify that we are handling a proper 8 bit binary number or signed int
    if len(num.replace("-", "")) > 3 and len(num) < 7 or len(num) > 8:
        print("Invalid Input!")
        __main__()

    # Verify that signed int is valid
    if len(num) <= 3:
        if int(num) > 127 or int(num) < -128:
            print("Invalid Integer")
            __main__()
        else:
            signed_int = True

    # Verify that binary value is valid
    if not signed_int:
        err = False
        for bit in num:
            if int(bit) != 0 and int(bit) != 1:
                print("Invalid Binary")
                err = True
                break
        if err:
            __main__()

    # Pass on our str to our handlers to process the conversions
    if signed_int:
        handle_int(num)
    else:
        handle_binary(num)


__main__()