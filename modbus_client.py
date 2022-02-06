from ast import literal_eval
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1",200)
final_response=""

# write multiple coils (function code in decimal: 15)
# inputData="0B 0F 001B 0009 02 4D02 6CA7"
# to test what's written use this below
# inputData ="01 01 001B 000F ED6E"

# write 1 coil (function code in decimal: 5)
# inputData ="01 05 0007 FF00 FC84"

# read coils (function code in decimal: 1)
# inputData ="01 01 0001 000D ED6E"

# write single register (function code in decimal: 6)
# inputData ="02 06 0004 0020 7604"

# read single register (function code in decimal: 3)
# inputData ="02 03 0004 0001 1162"

# write to multiple registers (function code in decimal: 16)
# inputData ="0B 10 0012 0002 04 0005 0070 A0D5"

# read from multiple registers (function code in decimal: 3)
# inputData ="0B 03 0012 0002 7687"

# write/read multiple registers (function code in decimal: 23)
# inputData ="01 17 0000 0002 0FFF 0002 04 ABCD 1234 4025"
# (testing first part of the fucntion) to test written stuff and read them, this is write method executed first then the line above
# inputData ="01 10 0000 0002 04 0005 0070 A0D5"
# (testing second part of the fucntion) to read things that I already wrote with this fucntion which means 
# execute the function first the line above (line number 10) then read them with this line below 
# inputData ="01 03 0FFF 0002 7687"

def modbus_actions(inputData):
    convertedToDecimal=[]
    inputData=inputData.split()
    for index in range(len(inputData)):
        toConvert=inputData[index]
        convertedToDecimal.append(int(toConvert, 16))
    print(convertedToDecimal)

    slaveAddress=convertedToDecimal[0]
    print("Slave adress  " + str(slaveAddress))


    if(convertedToDecimal[1]==1):
        print('Read coils, single bit access')
        value=client.read_coils(convertedToDecimal[2],convertedToDecimal[3])
        newList=[]
        for i in value.bits:
            newList.append(int(i))
        final_response=str(value)+ '\n'+ str(newList)
        
    elif (convertedToDecimal[1]==3):
        print('Read holding registers, 16 bit access')
        value = client.read_holding_registers(convertedToDecimal[2],convertedToDecimal[3])
        final_response=str(value)+ '\n'+ str(value.registers)
        
    elif (convertedToDecimal[1]==5):
        print('Write single coil, single bit access')
        value=0
        if(inputData[3]=="FF00"):
            value=1
        else:
            value=0
        result=client.write_coil(address=convertedToDecimal[2],value=value)
        final_response=result
        
    elif (convertedToDecimal[1]==6):
        print('Write single register, 16 bit access')
        result=client.write_register(address=convertedToDecimal[2],value=convertedToDecimal[3])
        final_response=result
        
    elif (convertedToDecimal[1]==15):
        print('Write multiple coils, single bit access')
        first=inputData[5][:2]
        second=inputData[5][2:4]
        first1=bin(int(first,16))[2:]
        second1=bin(int(second,16))[2:]
        newList=[]
        if(len(first1)<8):
            first1='0'*(8-len(first1))+first1
        for i in range(len(first1)):
            newList.append(bool(int(first1[i])))
        if(len(second1)<8):
            second1='0'*(8-len(second1))+second1
        for i in range(len(second1)):
            newList.append(bool(int(second1[i])))
        result=client.write_coils(address=convertedToDecimal[2],values=newList)
        final_response=result


    elif (convertedToDecimal[1]==16):
        print('Write multiple registers, 16 bit access')
        newList=[]
        for i in range(convertedToDecimal[3]):
            newList.append(convertedToDecimal[5+i])
        result=client.write_registers(address=convertedToDecimal[2], values=newList)
        final_response=result
        
        
    elif (convertedToDecimal[1]==23):
        print('Read/Write multiple registers, 16 bit access')
        newList=[]
        for i in range(convertedToDecimal[5]):
            newList.append(convertedToDecimal[7+i])
        value=client.readwrite_registers(read_address=convertedToDecimal[2], read_count=convertedToDecimal[3],write_address=convertedToDecimal[4],write_registers=newList)
        final_response=str(value)+ '\n'+ str(value.registers)
        
    else:
        print('Error, communication type not supported !')
        final_response='Error, communication type not supported !'


    return final_response
    client.close()