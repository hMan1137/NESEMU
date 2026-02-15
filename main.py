
#THE 6502 BEING LITTLE ENDIAN--AND FULL BEING 2 BYTE--MEMORY ADDRESSES NEED TO BE ASSEMBLED IN THE CORRECT ORDER WITH THIS FUNCTION
def AssembleByte(low, high):
    return (high << 8) | low


#HERES A GIGANTIC DICTIONARY LOOKUP THAT'S GONNA COME IN HANDY LATER
#IT STORES IN THE FOLLOWING PATTERN: 'OPCODE: ['NAME OF INSTRUCTION', 'ADDRESSING MODE USED', NUMBER OF BYTES USED BY INSTRUCTION, LEAST NUMBER OF CLOCK CYCLES USED]'
operations = {0x69: ['ADC', 'IMM', 2, 2], 0x65: ['ADC', 'ZP0', 2, 3], 0x75: ['ADC', 'ZPX', 2, 4], 0x6D: ['ADC', 'ABS', 3, 4], 0x7D: ['ADC', 'ABX', 3, 4],
              0x79: ['ADC', 'ABY', 3, 4], 0x61: ['ADC', 'IZX', 2, 6], 0x71: ['ADC', 'IZY', 2, 5], 0x29: ['AND', 'IMM', 2, 2], 0x25: ['AND', 'ZP0', 2, 3],
              0x35: ['AND', 'ZPX', 2, 4], 0x2D: ['AND', 'ABS', 3, 4], 0x3D: ['AND', 'ABX', 3, 4], 0x39: ['AND', 'ABY', 3, 4], 0x21: ['AND', 'IZX', 2, 6],
              0x31: ['AND', 'IZY', 2, 5], 0x0A: ['ASL', 'ACC', 1, 2], 0x06: ['ASL', 'ZP0', 2, 5], 0x16: ['ASL', 'ZPX', 2, 6], 0x0E: ['ASL', 'ABS', 3, 6],
              0x1E: ['ASL', 'ABX', 3, 7], 0x90: ['BCC', 'REL', 2, 2], 0xB0: ['BCS', 'REL', 2, 2], 0xF0: ['BEQ', 'REL', 2, 2], 0x24: ['BIT', 'ZP0', 2, 3],
              0x2C: ['BIT', 'ABS', 3, 4], 0x30: ['BMI', 'REL', 2, 2], 0xD0: ['BNE', 'REL', 2, 2], 0x10: ['BPL', 'REL', 2, 2], 0x00: ['BRK', 'IMM', 2, 7],
              0x50: ['BVC', 'REL', 2, 2], 0x70: ['BVS', 'REL', 2, 2], 0x18: ['CLC', 'IMP', 1, 2], 0xD8: ['CLD', 'IMP', 1, 2], 0x58: ['CLI', 'IMP', 1, 2],
              0xB8: ['CLV', 'IMP', 1, 2], 0xC9: ['CMP', 'IMM', 2, 2], 0xC5: ['CMP', 'ZP0', 2, 3], 0xD5: ['CMP', 'ZPX', 2, 4], 0xCD: ['CMP', 'ABS', 3, 4],
              0xDD: ['CMP', 'ABX', 3, 4], 0xD9: ['CMP', 'ABY', 3, 4], 0xC1: ['CMP', 'IZX', 2, 6], 0xD1: ['CMP', 'IZY', 2, 5], 0xE0: ['CPX', 'IMM', 2, 2],
              0xE4: ['CPX', 'ZP0', 2, 3], 0xEC: ['CPX', 'ABS', 3, 4], 0xC0: ['CPY', 'IMM', 2, 2], 0xC4: ['CPY', 'ZP0', 2, 3], 0xCC: ['CPY', 'ABS', 3, 4],
              0xC6: ['DEC', 'ZP0', 2, 5], 0xD6: ['DEC', 'ZPX', 2, 6], 0xCE: ['DEC', 'ABS', 2, 6], 0xDE: ['DEC', 'ABY', 2, 7], 0xCA: ['DEX', 'IMP', 1, 2],
              0x88: ['DEY', 'IMP', 1, 2], 0x49: ['EOR', 'IMM', 2, 2], 0x45: ['EOR', 'ZP0', 2, 3], 0x55: ['EOR', 'ZPX', 2, 4], 0x4D: ['EOR', 'ABS', 3, 4],
              0x5D: ['EOR', 'ABX', 3, 4], 0x59: ['EOR', 'ABY', 3, 4], 0x41: ['EOR', 'IZX', 2, 6], 0x51: ['EOR', 'IZY', 2, 5], 0xE6: ['INC', 'ZP0', 2, 5],
              0xF6: ['INC', 'ZPX', 2, 6], 0xEE: ['INC', 'ABS', 3, 6], 0xFE: ['INC', 'ABX', 3, 7], 0xE8: ['INX', 'IMP', 1, 2], 0xC8: ['INY', 'IMP', 1, 2],
              0x4C: ['JMP', 'ABS', 3, 3], 0x6C: ['JMP', 'IND', 3, 5], 0x20: ['JSR', 'ABS', 3, 6], 0xA9: ['LDA', 'IMM', 2, 2], 0xA5: ['LDA', 'ZP0', 2, 3],
              0xB5: ['LDA', 'ZPX', 2, 4], 0xAD: ['LDA', 'ABS', 3, 4], 0xBD: ['LDA', 'ABX', 3, 4], 0xB9: ['LDA', 'ABY', 3, 4], 0xA1: ['LDA', 'IZX', 2, 6],
              0xB1: ['LDA', 'IZY', 2, 5], 0xA2: ['LDX', 'IMM', 2, 2], 0xA6: ['LDX', 'ZP0', 2, 3], 0xB6: ['LDX', 'ZPY', 2, 4], 0xAE: ['LDX', 'ABS', 3, 4],
              0xBE: ['LDX', 'ABY', 3, 4], 0xA0: ['LDY', 'IMM', 2, 2], 0xA4: ['LDY', 'ZP0', 2, 3], 0xB4: ['LDY', 'ZPX', 2, 4], 0xAC: ['LDY', 'ABS', 3, 4],
              0xBC: ['LDY', 'ABX', 3, 4], 0x4A: ['LSR', 'ACC', 1, 2], 0x46: ['LSR', 'ZP0', 2, 5], 0x56: ['LSR', 'ZPX', 2, 6], 0x4E: ['LSR', 'ABS', 3, 6],
              0x5E: ['LSR', 'ABX', 3, 7], 0xEA: ['NOP', 'IMP', 1, 2], 0x09: ['ORA', 'IMM', 2, 2], 0x05: ['ORA', 'ZP0', 2, 3], 0x15: ['ORA', 'ZPX', 2, 4],
              0x0D: ['ORA', 'ABS', 3, 4], 0x1D: ['ORA', 'ABX', 3, 4], 0x19: ['ORA', 'ABY', 3, 4], 0x01: ['ORA', 'IZX', 2, 6], 0x11: ['ORA', 'IZY', 2, 5],
              0x48: ['PHA', 'IMP', 1, 3], 0x08: ['PHP', 'IMP', 1, 3], 0x68: ['PLA', 'IMP', 1, 4], 0x28: ['PLP', 'IMP', 1, 4], 0x2A: ['ROL', 'ACC', 1, 2],
              0x26: ['ROL', 'ZP0', 2, 5], 0x36: ['ROL', 'ZPX', 2, 6], 0x2E: ['ROL', 'ABS', 3, 6], 0x3E: ['ROL', 'ABX', 3, 7], 0x6A: ['ROR', 'ACC', 1, 2],
              0x66: ['ROR', 'ZP0', 2, 5], 0x76: ['ROR', 'ZPX', 2, 6], 0x6E: ['ROR', 'ABS', 3, 6], 0x7E: ['ROR', 'ABX', 3, 7], 0x40: ['RTI', 'IMP', 1, 6],
              0x60: ['RTS', 'IMP', 1, 6], 0xE9: ['SBC', 'IMM', 2, 2], 0xE5: ['SBC', 'ZP0', 2, 3], 0xF5: ['SBC', 'ZPX', 2, 4], 0xED: ['SBC', 'ABS', 3, 4],
              0xFD: ['SBC', 'ABX', 3, 4], 0xF9: ['SBC', 'ABY', 3, 4], 0xE1: ['SBC', 'IZX', 2, 6], 0xF1: ['SBC', 'IZY', 2, 5], 0x38: ['SEC', 'IMP', 1, 2],
              0xF8: ['SED', 'IMP', 1, 2], 0x78: ['SEI', 'IMP', 1, 2], 0x85: ['STA', 'ZP0', 2, 3], 0x95: ['STA', 'ZPX', 2, 4], 0x8D: ['STA', 'ABS', 3, 4],
              0x9D: ['STA', 'ABX', 3, 5], 0x99: ['STA', 'ABY', 3, 5], 0x81: ['STA', 'IZX', 2, 6], 0x91: ['STA', 'IZY', 2, 6], 0x86: ['STX', 'ZP0', 2, 3],
              0x96: ['STX', 'ZPX', 2, 4], 0x8E: ['STX', 'ABS', 3, 4], 0x84: ['STY', 'ZP0', 2, 3], 0x94: ['STY', 'ZPX', 2, 4], 0x8C: ['STY', 'ABS', 3, 4],
              0xAA: ['TAX', 'IMP', 1, 2], 0xA8: ['TAY', 'IMP', 1, 2], 0xBA: ['TSX', 'IMP', 1, 2], 0x8A: ['TXA', 'IMP', 1, 2], 0x9A: ['TXS', 'IMP', 1, 2],
              0x98: ['TYA', 'IMP', 1, 2]}
class _6502:



    def __init__(self):
        #THE NES USES A RESET VECTOR, SO WE'RE INITIALISING AS IF HAVING JUST DONE A RESET
        self.ACC = 0
        self.IXX = 0
        self.IXY = 0
        #THE STACK ITSELF OPERATES BETWEEN 0x0100 AND 0x01FF, THE STACK POINTER COUNTS BACKWARDS FROM 0xFF TO 0x00 AND IS ADDED TO 0x100 TO FETCH FROM THE STACK
        self.SP = 0xFD #SP GOES FROM 0x00 TO 0xFF, BUT WHEN RESETTING RUNS A FEW DUMMY CYCLES BRINGING THE SP DOWN A COUPLE NOTCHES, WHICH IS WHY ITS FD AND NOT FF
        self.SR = 0x20 #CORRESPONDS TO BIT 5, WHICH IS UNUSED AND ALWAYS PUSHES TO 1
        self.Flag = {'C': False, 'Z': False, 'I': False, 'D': False, 'B': False, 1: True, 'V': False, 'N': False} #A VARIABLE TO STORE WHAT FLAGS ARE SET AT ANY INSTANT....
        #...IF THEY ARE SET THEY WILL BE TRUE, ELSE THEY WILL BE FALSE
        self.RAM = bytearray(65536) #RAM HAS A FULL ADDRESSABLE RANGE OF 64KB, SO BETWEEN 0x0000 and 0xFFFF. IT'S CHOPPED UP IN WEIRD WAYS THOUGH, LIKE THE FIRST TWO KB MIRROR THREE MORE TIMES
        self.addr = 0x0000 #KIND OF A MISNOMER, ITS ACTUALLY THE DATA AT The ADDRESS BUT IMTOO LAZY TO CHANGE IT RIGHT NOW
        self.PC = AssembleByte(self.RAM[0xFFFC], self.RAM[0xFFFD]) #THIS IS WHERE THE RESET POSITION FOR THE PC IS LOCATED. USUALLY IT'S EQUAL TO 0x8000 BUT ITS MORE...
        #...INTELLIGENT TO MATHEMATICALLY CALCULATE IT LIKE THE 6502 DID SINCE ITS NOT ACTUALLY A HARD-CODED THING, SO THERE COULD BE A WEIRD CASE WHERE IT DOES NOT...
        #...RESET TO 0x8000
        self.cycle = -1 #A VARIABLE COUNTING DOWN ON THE NUMBER OF CLOCK CYCLES LEFT ON AN INSTRUCTION. NEEDED TO KNOW WHEN IT CAN LEGALLY MOVE ON TO THE NEXT INSTRUCTION
        self.AddCycle = [0, 0] #WILL ADD A CYCLE IF BOTH ELEMENTS ARE ONE. ADDRESSING MODE WILL TURN ON THE FIRST ELEMENT, THE INSTRUCTION WILL TURN ON THE SECOND


    #A DETERMINER FUNCTION FOR KNOWING WHAT ADDRESS MODE WE'RE WORKING WITH AND THUS PERFORMING THE APPROPRIATE ADDRESSING MODE FUNCTION. THE ADDRESSING MODES ARE DEALT WITH...
    #...A LITTLE LATER
    def UseMode(self, mode):
        if mode == 'IMP':
            return self.IMP()
        elif mode == 'IMM':
            return self.IMM()
        elif mode == 'ABS':
            return self.ABS()
        elif mode == 'ABX':
            return self.ABX()
        elif mode == 'ABY':
            return self.ABY()
        elif mode == 'IZX':
            return self.IZX()
        elif mode == 'IZY':
            return self.IZY()
        elif mode == 'REL':
            return self.REL()
        elif mode == 'ZP0':
            return self.ZP0()
        elif mode == 'ZPX':
            return self.ZPX()
        elif mode == 'ZPY':
            return self.ZPY()
        elif mode == 'IND':
            return self.IND()
        elif mode == 'ACC': #some commands address the accumulator directly, so we're gonna deal with that separately here
            return -1
        else:               #CATCH-ALL FOR ANYTHING ILLEGAL
            return -2

    #FUNCTIONS THAT READ FROM AND WRITE TO THE ADDRESS

    def read(self, mode):
        address = self.UseMode(mode)
        self.addr = self.ACC if address == -1 else self.RAM[address]
        return address #RETURNING THE INDEX OF RAM WE CHECK AT FOR THE SAKE OF WRITING CHANGES DIRECTLY TO MEMORY
    def write(self, data, address):
       # Mode = self.UseMode(mode)
       if address== -1:
           self.ACC = data
       else:
           self.RAM[address] = data
    #WRITES AT THE CURRENT INDEX BEFORE THE PC INCREMENTS

    #OKAY, THIS IS IMPORTANT. WE NEED TO WORK ON ALL THE ADDRESSING MODES. THE NES HAS APPROXIMATELY ONE BAJILLION OF THEM
    #FOR THIS, WE NEED TO UNDERSTAND OPCODE STRUCTURE. IT'S BASICALLY AAABBBCC, WHERE BBB TELLS YOU THE ADDRESSING MODE.

    #THE 6502 USES SOMETHING CALLED 'ZERO-PAGE' ADDRESSING, WHICH CAN LIMIT THE ADDRESSABLE MEMORY RANGE TO THE FIRST 256 BYTES OF MEMORY ASSIGNED TO BE ZERO-
    #PAGE MEMORY.

    #WE ALREADY HAVE A DETERMINER FUNCTION FOR ALL THE ADDRESSING MODES, SO NOW WE JUST NEED TO DEFINE THEM

    #IT IS FUNDAMENTALLY IMPORTANT TO REMEMBER THAT SINCE THIS IS A VON NEUMANN ARCHITECTURE, THE INSTRUCTIONS LIVE IN THE SAME MEMORY SPACE AS THE OPERANDS. THE PC POINTS TO...
    #...THE CURRENT INSTRUCTION OPCODE BEING PERFORMED, BUT PC+1 WOULD POINT TO THE OPERAND, OR AT LEAST PART OF IT, SINCE THAT ALWAYS COMES RIGHT AFTER

    #THE FIRST TWO ARE HELPER FUNCTIONS
    def ZeroPage(self, addr):
        return AssembleByte(self.RAM[addr & 0x00FF], self.RAM[(addr + 1) & 0x00FF])
        #BASICALLY JUST PERFORMS A WRAP ON WHATEVER ADDRESS WE GET IS BETWEEN BYTE 1 AND 256
    # NEXT, WE'LL NEED A FUNCTION FOR FETCHING THE RELATIVE ADDRESS WHEN USING RELATIVE ADDRESSING, WHICH GETS THE ADDRESS BY ADDING AN OFFSET TO THE PC

    def GetByte(self, noINC = False):
        val = self.RAM[self.PC]
        if not noINC: #NEW CHANGE...
            self.PC += 1 #INCREMENTS PROGRAM COUNTER PER BYTE FETCHED, MORE CYCLE ACCURATE THAN THE PREVIOUS VERSION WHERE I WOULD INCREASE IT ALL AT ONCE AT THE END OF THE INSTRUCTION
        return val
    def IMP(self): #IMPLIED ADDRESSING, SO THERE ISNT REALLY AN OPERAND
        return 0 #HEY THAT ONE WAS PRETTY EASY!
    def IMM(self): #IMMEDIATE ADDRESSING, THE OPERAND IS THE NEXT BYTE
        return self.PC + 1
    def IND(self): #USED TO DEFERENCE FOR A JMP INSTRUCTION. IT JMPS TO THE ADDRESS FOUND ON THE ADDRESS THE PROGRAM TAKES IT
        lb = self.GetByte()
        hb = self.GetByte()
        low = self.RAM[AssembleByte(lb, hb)] & 0xFF #DEREFENCES FOR THE LOW POINTER
        high = self.RAM[(AssembleByte(lb, hb + 1))] &0xFF #DEFERENCES FOR THE HIGH POINTER
        return AssembleByte(low, high)

        #OKAY SO HERES SOMETHING FUNKY: TURNS OUT THE 6502 HAS A WEIRD BUG. WHEN THE LOW POINTER IS 256, OBVIOUSLY THE HIGH POINTER WOULD ADD ONE THUS CHANGING THE PAGE....
        #...BUT THE JUMP INSTRUCTION SIMPLY DOESNT DO THAT; IT IGNORES THE +1. PROBABLY WONT NEED TO IMPLEMENT THE BUG FOR NOW, BUT IT IS GOOD TO KNOW.
    def ABS(self): #ABSOLUTE ADDRESSING
        return AssembleByte(self.GetByte(), self.GetByte())

    def ABX(self): #ABSOLUTE ADDRESSING WITH AN X REGISTER OFFSET
        return AssembleByte(self.GetByte(), self.GetByte()) + self.IXX

    def ABY(self): #ABSOLUTE ADDRESSING WITH A Y REGISTER OFFSET
        return AssembleByte(self.GetByte(), self.GetByte()) + self.IXY

    def IZX(self): #INDIRECT ZERO-PAGE ADDRESSING WITH X REGISTER OFFSET
        return self.ZeroPage(self.GetByte() + self.IXX)

    def IZY(self): #SAME THING WITH Y-OFFSET, EXCEPT ITS ACTUALLY THE FINAL ADDRESS THATS OFFSET FOR SOME REASON
        var = self.ZeroPage(self.GetByte())
        return var + self.IXY

    def REL(self): #THIS ONES WEIRD...IT BASICALLY TAKES THE ADDRESS POINTED TO BY THE PC AND TURNS IT INTO A SIGNED OFFSET BETWEEN -128 AND 127
        #ALL WE NEED TO RETURN HERE IS THE BYTE CONVERTED TO SIGNED
       # if self.GetByte(1) & 0x80: #AND WITH BINARY 10000000, so we're basically checking if the number is 128 or bigger
            val =self.GetByte()
            self.AddCycle[0] = 1
            return val - 0x100  if val & 0x80 else val #SUBTRACT 256 TO MAKE IT WRAP TO NEGATIVE

        #else:
         #   return self.GetByte(1) #RETURN AS IS IF LESS THAN 128
    def ZP0(self): #THIS IS ONLY A ONE BYTE OPERAND SO I CANT JUST USE ZeroPage HERE, EXACT SAME PRINCIPLE THOUGH
        return self.GetByte() & 0x00FF

    #THESE ARE THE SAME BUT WITH X AND Y OFFSET
    def ZPX(self):
        return (self.GetByte() + self.IXX) & 0x00FF
    def ZPY(self):
        return (self.GetByte() + self.IXY) & 0x00FF


    #AND NOW, WE SHALL DO ALL THE OPCODES. THERE'S 200-SOMETHING POSSIBLE OPCODE ENTRIES ON THE 6502, BUT THERE ARE ONLY ABOUT 151 LEGAL ONES ON THE NES (56 ARE ACTUALLY...
    #...DIFFERENT. THE INFLATED NUMBER IS BECAUSE MANY OF THE SAME INSTRUCTIONS USE MULTIPLE ADDRESSING MODES)
    #THE ILLEGAL OPCODES ARE USED BY A SMALL PERCENTAGE OF GAMES SO I WILL IMPLEMENT THEM EVENTUALLY, BUT THE VAST MAJORITY DO NOT NEED THEM, SO I'M SKIPPING THEM FOR NOW

    #BEFORE WE DO ANYTHING HERE THOUGH, THE 6502 NEEDS A FEW THINGS TO BE ABLE TO PERFORM THESE AT ALL
    #THIS GETS THE DATA WE'RE WORKING WITH FOR AN OPCODE
    def fetch(self):
        opcode = self.RAM[self.PC]
        self.PC += 1
        Mode = operations[opcode][1]

        return self.read(Mode) #NOW THAT WE HAVE THE MODE, WE RUN IT THROUGH READ TO SET SELF.ADDR TO THE OPERAND, THIS RETURNS THE RETURN INDEX OF INSTRUCTION
    def clock(self):
        opcode =self.RAM[self.PC] #A FUNCTION TELLING THE CPU THAT ONE CLOCK CYCLE HAS PASSED
        if self.cycle == 0:
            self.PC += 1 #INCREMENT THE COUNTER, THE INSTRUCTION HAS BEEN COMPLETED IF CYCLES IS ZERO
            self.cycle = operations[opcode][3]
        elif self.cycle > 0:
            self.cycle -= 1
    def reset(self): #THAT RESET VECTOR I WAS TALKING ABOUT EARLIER
        #JUST REINITIALISES EVERYTHING TO HOW IT WAS
        self.ACC = 0
        self.IXX = 0
        self.IXY = 0
        #
        self.SP = 0xFD
        self.SR = 0x20  # CORRESPONDS TO BIT 5, WHICH IS UNUSED AND ALWAYS PUSHES TO 1
        self.Flag = {'C': False, 'Z': False, 'I': False, 'D': False, 'B': False, 1: True, 'V': False,
                     'N': False}
        self.addr = 0x0000
        self.PC = AssembleByte(self.RAM[0xFFFC], self.RAM[0xFFFD])

    def irq(self):#AN INTERRUPT REQUEST SIGNAL
        if not self.Flag['I']: #IF INTERRUPTS ARE NOT DISABLED
            self.PC += 2 #YOU ACTUALLY FETCH THE INSTRUCTION BYTE THEN GET THE NEXT BYTE, BUT BOTH THINGS ARE DISCARDED, SO EFFECTIVELY ONLY THE INCREMENT OCCURS
            self.Push((self.PC >> 8) & 0xFF )#PUSH THE PROGRAM COUNTER STATE TO THE STACK
            self.Push((self.PC & 0xFF))
            #SET THE B FLAG CLEAR AND THE INTERRUPT DISABLE FLAG ON, THEN PUSH THE STATUS FLAG TO THE STACK
            self.SetSignal('B', False)
            self.SetSignal('I', True)
            self.Push(self.MakeSF())
            #SET THE PROGRAM COUNTER TO AN ADDRESS BETWEEN 0xFFFE AND 0xFFFF, which is where the IRQ vector is located
            self.PC = AssembleByte(self.RAM[0xFFFE], self.RAM[0xFFFF])

    def nmi(self):#A NON MASKABLE INTERRUPT. THESE ONES CAN NEVER BE IGNORED, UNLIKE THE REGULAR IRQs. OTHER THAN THAT, THEY ARE ALMOST IDENTICAL
            self.PC += 2

            self.Push((self.PC >> 8) & 0xFF)  # PUSH THE PROGRAM COUNTER STATE TO THE STACK
            self.Push((self.PC & 0xFF))
            # SET THE B FLAG CLEAR AND THE INTERRUPT DISABLE FLAG ON, THEN PUSH THE STATUS FLAG TO THE STACK
            self.SetSignal('B', False)
            self.SetSignal('I', True)
            self.Push(self.MakeSF())
            # SET THE PROGRAM COUNTER TO AN ADDRESS BETWEEN 0xFFFA AND 0xFFFB, which is where the NMI vector is located
            self.PC = AssembleByte(self.RAM[0xFFFA], self.RAM[0xFFFB])

    # JUST SIMPLE MODULES TO PUSH AND POP FROM THE STACK
    def Push(self, data):
        self.RAM[self.SP | 0x100] = data
        # SP COUNTS BACKWARDS SO IT DECREMENTS
        self.SP -= 1

    def Pop(self):
        self.SP += 1
        return self.RAM[self.SP | 0x100]

    #A SIMPLE FUNCTION TO TURN A SPECIFIC FLAG ON OR OFF WHEN CALLED
    def SetSignal(self, F, on):    #WE WILL DEFINE WHAT ALL THE BITS IN THE STATUS FLAG CORRESPOND TO
        #HERE ARE ALL THE FLAGS IN ORDER
        # C: Carry, turns on if a carry must be performed, 0x01
        # Z: Zero Flag, turns on if the result of a calculation was zero, 0x02
        # I: Interrupt Disable, turns on to trigger interrupt ignore for regular IRQ, 0x04
        # D: Decimal, not actually used in the NES but still there for some reason, 0x08
        # B: B flag, doesnt actually do anything in the CPU but is useful to some software, 0x10
        # 1: 1 flag, no use at all, pushes to one by default, 0x20
        # O: Overflow flag, turns on if two negative numbers add to a positive or vice versa, 0x40
        # N: Negative flag, turns on if the result of a mathematical addition or subtraction could be negative when using two's complement, 0x80
        self.Flag[F] = (on == 1)

    #EACH INSTRUCTION HAS A SPECIFIC NUMBER OF FLAGS THAT ITS CAPABLE OF TURNING ON OR OFF DEPENDING ON THE RESULT. I HAVE MENTIONED ALL THE FLAGS NEXT TO EACH INSTRUCTION
    #HERE ARE THE ACTUAL INSTRUCTIONS
    def MakeSF(self): #GENERATES A STATUS FLAG BYTE BASED ON THE FLAGS THAT ARE ON OR OFF. THIS IS SOMETIMES NEEDED IN CERTAIN INSTRUCTIONS
        return 0x80 * self.Flag['N'] + 0x40 * self.Flag['V'] + 0x20 * self.Flag[1] + 0x10 * self.Flag['B'] + 0x08 * self.Flag['D'] + 0x04 * self.Flag['I'] + 0x02 * self.Flag['Z'] + 0x01 * self.Flag['C']
    def BreakSF(self, byte): #GENERATES STATUS FLAGS FROM A STATUS FLAG BYTE
        self.SetSignal('C', byte & 0x01 > 0)
        self.SetSignal('Z', byte & 0x02 > 0)
        self.SetSignal('I', byte & 0x04 > 0)
        self.SetSignal('D', byte & 0x08 > 0)
        self.SetSignal('B', byte & 0x10 > 0)
        self.SetSignal(1 , byte & 0x20 > 0)
        self.SetSignal('V', byte & 0x40 > 0)
        self.SetSignal('N', byte & 0x80 > 0)
    def ADC(self): #ADD WITH CARRY. C, V, N, Z
        #THIS FUNCTION IS BY FAR THE BIGGEST HEADACHE TO FIGURE OUT
        self.fetch()
        base = self.addr + self.ACC
        val = base + (self.Flag['C']) #NEEDS TO ADD THE VALUE OF THE CARRY
        self.ACC = val & 0x00FF  # NEEDS TO WRAP TO 255/-128/127
        self.SetSignal('C', val > 0x00FF) #SETS THE CARRY BIT ON IF THE ADDITION WAS GREATER THAN 8 BITS
        #OKAy, EASY ENOUGH, RIGHT? WRONG!!!! BECAUSE YOU HAVE TO FIGURE OUT EVERYTHING THAT SETS THE OTHER FLAGS, TOO!

        #OKAY, ZERO FLAG; THIS ONE'S EASY, JUST CHECK IF THE RESULT ENDS UP BEING ZERO
        self.SetSignal('Z', val & 0x00FF == 0)  #THE AND WITH 255 IS JUST AN INSURANCE POLICY. SHOULDNT REALLY MATTER BUT ITS BEING EXTRA SAFE
        #THE NEGATIVE FLAG IS NOT AS TRIVIAL BUT IT'S EASY ENOUGH TO DIGEST...
        #BASICALLY, WE ARE CHECKING IF THE TWO NUMBERS THAT WE ADDED UP WOULD THEORETICALLY GIVE US A NEGATIVE NUMBER IF THEY WERE IN TWO'S COMPLEMENT. SINCE THE MAX...
        #...POSITIVE RANGE IN TWO's COMPLEMENT FOR 1 BYTE IS 127, IF THE ADDITION WAS GREATER THAN THAT, IT WOULD WRAP AROUND TO SOME OFFSET FROM -128. HENCE, WE JUST...
        #...NEED TO CHECK IF THE VALUE IS GREATER THAN 127. IN EVEN SIMPLER TERMS, WE'RE JUST CHECKING IF THE MOST SIGNIFICANT BIT WOULD BE ON
        self.SetSignal('N', val > 127)

        #OKAY, THIS ONE'S A DOOZY...HOW DO WE CHECK FOR OVERFLOW? WELL, OVERFLOW OCCURS IN ONE OF TWO CASES, BOTH ASSUMING TWO'S COMPLEMENT LOGIC:
        #1. YOU ADDED TWO POSITIVE NUMBERS, BUT ENDED UP GETTING A NEGATIVE NUMBER
        #2. YOU ADDED TWO NEGATIVE NUMBERS, BUT ENDED UP GETTING A POSITIVE NUMBER
        # AFTER SOME THINKING I HAVE FIGURED OUT A LOGICAL EXPRESSION...
        # NOT(A XOR B) AND ((A&B) XOR C) WHERE A AND B ARE THE MSB OF THE ACC AND RAM, AND C IS THE MSB OF THE RESULT OF THE ADDITION
        self.SetSignal('V', 0x0080 & (~(self.ACC ^ self.addr ) & ((self.ACC & self.addr) ^ val))) #AND WITH 0x0080 LIMITS IT TO THE MSB
        #OKAY, WHY DID THAT WORK? BASICALLY: WHEN YOU HAVE TWO POSITIVE NUMBERS ADDED TOGETHER IN TWO'S COMPLEMENT, BOTH OF THEIR MSBs ARE 0. IF THE RESULTING NUMBER IS...
        #...NEGATIVE, ITS MSB IS 1, AND THE OPPOSITE IS ALSO TRUE. THAT MEANS OVERFLOW OCCURS WHEN THE MSB OF THE NUMBERS YOU ADD IS DIFFERENT FROM THE RESULT, HENCE...
        #...((A AND B) XOR C). THE ONLY PROBLEM WITH THIS EXPRESSION IS THAT IT CAN TRIGGER TRUE WHEN A AND B ARE DIFFERENT FROM EACH OTHER, BUT IT SHOULD NEVER BE TRUE...
        #...SO THAT MEANS YOU WANT THE ENTIRE EXPRESSION TO BE FALSE IF A AND B ARE DIFFERENT, HENCE THE NOT(A XOR B) AT THE START.
        #PHEW! THAT ONE WAS PRETTY CEREBRAL, BUT APPARENTLY NOTHING IS AS COMPLICATED AFTER SBC.

    def SBC(self): #SUBTRACT WITH BORROW, C, V, N, Z
        #BORROW EFFECTIVELY MEANS NOT(CARRY)

        self.fetch()
        base = self.ACC - self.addr
        val = base - (1-self.Flag['C'])
        self.ACC = val & 0x00FF
        self.SetSignal('C', val < 0x0000) #IT COULD NEVER REACH THE UPPER LIMIT OF 255, SO HERE A CARRY OCCURS WHEN IT REACHES THE LOWER LIMIT OF 0
        self.SetSignal('Z', val & 0x00FF == 0)
        self.SetSignal('N', val > 127)
        self.SetSignal('V', 0x0080 & ((self.ACC ^ self.addr) & ((self.ACC & self.addr) ^ val))) #HERE, IT IS THE SAME EXCEPT THE NOT FROM THE XOR IS REMOVED BECAUSE...
        #...OVERFLOW IN SUBTRACTION CAN ONLY OCCUR WHEN BOTH NUMBERS HAVE *DIFFERENT* MSBs, WHICH IS BECAUSE SUBTRACTING A FROM B IS THE SAME THING AS ADDING THE...
        #...COMPLEMENT OF A FROM B. SO, SUBTRACTING DIFFERENT MSBs BECOMES THE SAME AS ADDING THE SAME MSBs
    def AND(self): #BITWISE AND. Z, N
        self.fetch()
        self.ACC = self.ACC & self.addr
        self.SetSignal('N', self.ACC & 0x80 != 0)
        self.SetSignal('Z', self.ACC & 0x00FF == 0)
    def LSL(self): #LOGICAL LEFT SHIFT TO EITHER ACC OR VALUE. C, Z, N
        mode = self.fetch()
        if mode == 'ACC':
            #THE CARRY IS SET IF THE INITIAL VALUE HAD BIT 7 ON
            self.SetSignal('C', self.ACC & 0x80 != 0)
            self.ACC = self.ACC << 1
            #THE NEGATIVE IS SET IF THE NEW BIT-SHIFTED VALUE HAS BIT 7 ON
            self.SetSignal('N', self.ACC & 0x80 != 0)

        else:
            self.SetSignal('C', self.addr & 0x80 != 0)
            self.addr = self.addr << 1
            self.SetSignal('N', self.addr & 0x80 != 0)
    def BCC(self):
        self.fetch()
        if not self.Flag['C']:  #BRANCH IF CARRY CLEAR. INCREMENTS THE PC BY 2, THEN ADDS THE RELATIVE OFFSET IF THE CARRY IS CLEAR
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr #THIS ONLY USES RELATIVE MODE, SO THE ADDRESS IS CONVERTED TO SIGNED BEFOREHAND (SEE REL())

    def BCS(self): #BRANCH IF CARRY SET. IDENTICAL TO BCC, JUST WITH THE CONDITION FLIPPED
        self.fetch()
        if self.Flag['C']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BEQ(self):
        self.fetch() #BRANCH IF EQUAL. DOES THE SAME THING IF THE ZERO FLAG IS SET
        if self.Flag['Z']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BIT(self): #BIT TEST. Z,V, N. THIS OPERATION ONLY CHANGES FLAGS. IT PERFORMS A BITMASK OF ACC & ADDR, SETTING ZERO IF THE RESULT IS ZERO. V AND N ARE SIMPLY...
        #...THE VALUES OF BIT 6 AND 7 OF ADDR.
        self.fetch()
        self.SetSignal('Z', ~(self.ACC & self.addr))
        self.SetSignal('N', (self.addr & 0x0080))
        self.SetSignal('V', (self.addr & 0x0040))
    def BMI(self): #BRANCH IF MINUS. SAME AS THE PREVIOUS BRANCHES FOR THE NEGATIVE FLAG
        self.fetch()
        if self.Flag['N']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BNI(self): #BRANCH IF NOT EQUAL. (THE ZERO FLAG IS CLEAR)
        self.fetch()
        if not self.Flag['Z']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BPL(self): #BRANCH IF PLUS. (THE NEGATIVE FLAG IS CLEAR)
        self.fetch()
        if not self.Flag['N']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BRK(self): #BREAK (ALSO KNOWN AS A SOFTWARE IRQ). I, B.
        #THIS ONE'S INTERESTING. WE PUSH THE INCREMENTED PROGRAM COUNTER TO THE STACK AND THEN PUSH ALL THE FLAGS TO THE STACK, AFTER WHICH WE SET THE PC TO A SPECIFIC VALUE
        self.fetch()
        self.Push((self.PC >> 8) & 0xFF) #GETS THE HIGH BYTE FIRST
        self.Push(self.PC & 0xFF) #GETS THE LOW BYTE SECOND
        #WE PUSH IT IN LITTLE ENDIAN WHEN THE MEMORY HOLDS BIG ENDIAN, BUT IT WORKS OUT SINCE THE STACK COUNTS BACKWARDS
        self.Push(self.MakeSF())
        #INTERRUPT DISABLE AND B IS SET TO 1 AFTER PUSHING
        self.SetSignal('I', 1)
        self.SetSignal('B', 1)
        self.PC = 0xFFFE
        #THIS INTERRUPT IS TECHNICALLY NON MASKABLE, SO ITS USEFUL AS A SOFT INTERRUPT THAT A PROGRAM CAN EXECUTE AT ANY TIME, MAINLY FOR CRASH HANDLING
    def BVC(self): #BRANCH IF OVERFLOW CLEAR.
        self.fetch()
        if not self.Flag['V']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BVS(self): #BRANCH IF OVERFLOW SET
        self.fetch()
        if self.Flag['V']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def CLC(self): #CLEAR THE CARRY. SELF EXPLANATORY
        self.fetch()
        self.SetSignal('C', 0)
    def CLD(self): #CLEAR THE DECIMAL. THIS WAS USUALLY USED TO ENABLE BCD, BUT THIS IS DISABLED IN THE NES. IT IS, HOWEVER, STILL THERE FOR STATE-STORAGE
        self.fetch()
        self.SetSignal('D', 0)
    def CLI(self): #ClEAR THE INTERRUPT DISABLE
        self.fetch()
        self.SetSignal('I', 0)
    def CLV(self): #CLEAR THE OVERFLOW
        self.fetch()
        self.SetSignal('V', 0)
    def CMP(self): #COMPARE A. COMPARES ACC WITH A VALUE IN MEMORY, SETTING FLAGS AS APPROPRIATE. C, Z, N
        self.fetch()
        val = self.ACC - self.addr
        self.SetSignal('C', val >= 0)
        self.SetSignal('Z', val == 0)
        self.SetSignal('N', val < 0)
    def CPX(self): #COMPARE X. SAME THING WITH REGISTER X. C, Z, N
        self.fetch()
        val = self.IXX - self.addr
        self.SetSignal('C', val >= 0)
        self.SetSignal('Z', val == 0)
        self.SetSignal('N', val < 0)
    def CPY(self): #COMPARE Y. SAME THING WITH REGISTER Y. C, Z, N
        self.fetch()
        val = self.IXY - self.addr
        self.SetSignal('C', val >= 0)
        self.SetSignal('Z', val == 0)
        self.SetSignal('N', val < 0)
    def DEC(self):#DECREMENT MEMORY. SUBTRACT ONE FROM A MEMORY LOCATION. WRITES BACK TO MEMORY/ ACC.Z. N

        fetched = self.fetch()
        self.write(self.addr - 1, fetched)
        self.SetSignal('Z', self.addr - 1 == 0)
        self.SetSignal('N', ((self.addr - 1) & 0x80 != 0))
    def DEX(self): #DECREMENT X. SAME THING BUT FOR THE X REGISTER. Z, N
        self.fetch()
        self.IXX -= 1
        self.SetSignal('Z', self.IXX== 0)
        self.SetSignal('N', (self.IXX & 0x80 != 0))
    def DEY(self): #DECREMENT Y. SAME THING BUT FOR THE Y REGISTER. Z, N
        self.fetch()
        self.IXY -= 1
        self.SetSignal('Z', self.IXY== 0)
        self.SetSignal('N', (self.IXY & 0x80 != 0))
    def EOR(self): #EXCLUSIVE OR. EORs BETWEEN ACC AND ADDR, SETTING REGISTERS APPROPRIATELY. Z,N.
        self.fetch()
        self.ACC = self.ACC ^ self.addr
        self.SetSignal('Z', self.ACC == 0)
        self.SetSignal('N', self.ACC &0x80 !=0)
    def INC(self): #INCREMENT MEMORY. ADD ONE TO A MEMORY LOCATION. WRITES BACK TO MEMORY/ ACC. Z, N.
        fetched = self.fetch()
        self.write(self.addr + 1, fetched)
        self.SetSignal('Z', self.addr +1 == 0)
        self.SetSignal('N', ((self.addr+ 1) & 0x80!= 0))
    def INX(self): #INCREMENT X. SAME THING BUT FOR THE X REGISTER. Z, N.
        self.fetch()
        self.IXX += 1
        self.SetSignal('Z', self.IXX == 0)
        self.SetSignal('N', (self.IXX & 0x80 != 0))

    def INY(self):  # DECREMENT Y. SAME THING BUT FOR THE Y REGISTER. Z, N
        self.fetch()
        self.IXY += 1
        self.SetSignal('Z', self.IXY == 0)
        self.SetSignal('N', (self.IXY & 0x80 != 0))

    def JMP(self): #JUMP. PROGRAM COUNTER IS EQUAL TO THE SELF.ADDR.
        self.fetch()
        self.PC = self.addr
    def JSR(self): #JUMP TO SUBROUTINE. PUSHES CURRENT PC TO STACK THEN SETS IT TO SELF.ADDR. USED WHEN YOU WANT TO BE ABLE TO GO BACK FROM WHERE YOU JUMPED.
        self.fetch()
        self.Push((self.PC<< 8)& 0xFF)
        self.Push(self.PC & 0xFF)
        self.PC = self.addr
    def LDA(self): #LOAD A. LOADS SELF.ADDR INTO ACC. Z, N.
        self.fetch()
        self.ACC = self.addr
        self.SetSignal('Z', self.ACC == 0)
        self.SetSignal('N', self.ACC & 0x80 !=0)
    def LDX(self): #LOAD Y. LOADS SELF.ADDR INTO Y. Z, N.
        self.fetch()
        self.IXX = self.addr
        self.SetSignal('Z', self.IXX == 0)
        self.SetSignal('N', self.IXX & 0x80 !=0)
    def LDY(self): #LOAD Y. LOADS SELF.ADDR INTO Y. Z, N.
        self.fetch()
        self.IXY = self.addr
        self.SetSignal('Z', self.IXY == 0)
        self.SetSignal('N', self.IXY &0x80 != 0)
    def LSR(self): #LOGICAL SHIFT TO THE RIGHT. WRITES BACK TO MEMORY/ACC. C, Z, N. Carry becomes bit 0
        fetched = self.fetch()
        self.SetSignal('C', self.addr & 0x01 != 0)
        self.SetSignal('N', False)
        self.addr = self.addr >> 1
        self.SetSignal('Z', self.addr == 0)
        self.write(self.addr, fetched)
    def NOP(self): #NO OPERATION. JUST WASTES CPU CYCLES
        self.fetch()
        return
    def ORA(self): #BITWISE OR. ORs THE ACCUMULATOR WITH SELF.ADDR. Z, N.
        self.fetch()
        self.ACC = self.addr | self.ACC
        self.SetSignal('Z', self.ACC == 0)
        self.SetSignal('N', self.ACC & 0x80 !=0)
    def PHA(self): #PUSH A. SIMPLY PUSHES ACC TO THE STACK
        self.fetch()
        self.Push(self.ACC)
    def PHP(self): #PUSH PROCESSOR STATUS. PUSHES THE STATUS FLAGS AND PUSHES B AS 1. B
        self.fetch()
        self.SetSignal('B', True)
        self.Push(self.MakeSF())
    def PLA(self): #PULL A. POPS FROM STACK POINTER AND LOADS INTO ACC. Z, N.
        self.fetch()
        self.ACC = self.Pop()
        self.SetSignal('Z', self.ACC == 0)
        self.SetSignal('N', self.ACC & 0x80 !=0)
    def PLP(self): #PULL PROCESSOR STATUS. POPS FROM THE STACK AND LOADS INTO THE STATUS FLAGS. ALL THE FLAGS
        #NOTE THAT THE VALUE OF I CHANGING WILL TAKE EFFECT IN THE NEXT CYCLE, NOT IMMEDIATELY. IMPLEMENT THIS!!!
        self.fetch()
        byte = self.Pop()
        self.BreakSF(byte) #BREAKSF TAKES A BYTE REPRESENTING THE STATUS FLAGS AND CONVERTS THEM INTO THE DICTIONARY FLAGS BEING USED IN THE EMULATION
    def ROL(self): #SHIFTS ACC/ADDR TO THE LEFT, BUT ACTS AS IF THE CARRY BIT IS BOTH BELOW BIT 0 AND ABOVE BIT 7. CARRY IS SHIFTED TO BIT 0, AND BIT 7 IS THEN...
        #SHIFTED TO CARRY. THIS INSTRUCTION WRITES BACK TO MEMORY/ACC. C, Z, N.
        fetched = self.fetch()
        temp = self.addr << 1
        temp = temp + self.Flag['C'] #CARRY SHIFTED INTO BIT 0

        self.SetSignal('C', self.addr & 0x0080 != 0) #CARRY EQUAL TO BIT 7

        self.SetSignal('N', temp & 0x80 !=0)
        self.SetSignal('Z', temp == 0)
        self.write(temp, fetched)
    def ROR(self): #SHIFTS ACC/ADDR TO THE RIGHT. SAME THING BUT THE OTHER WAY AROUND. C, Z, N.
        fetched = self.fetch()
        temp = self.addr >> 1
        temp = temp + (self.Flag['C'] << 7)  # CARRY SHIFTED INTO BIT 7

        self.SetSignal('C', self.addr & 0x01 != 0)  # CARRY EQUAL TO BIT 0

        self.SetSignal('N', temp & 0x80 !=0)
        self.SetSignal('Z', temp == 0)
        self.write(temp, fetched)
    def RTI(self): #RETURN FROM INTERRUPT. POPS THE STATUS FLAGS FROM THE STACK, THEN POPS THE PC
        #ONE IMPORTANT THING TO NOTE HERE IS THAT THE INTERRUPT RETURN WILL BE IMMEDIATE, NOT DELAYED ONE CYCLE
        self.fetch()
        byte = self.Pop()
        self.BreakSF(byte)
        self.PC = self.Pop() + (self.Pop() << 8) #HIGH BYTE COMES IN SECOND, SO IT NEEDS TO BE ASSEMBLED CORRECTLY
    def RTS(self): #RETURN FROM SUBROUTINE. POPS ADDRESS FROM STACK INTO PC, THEN INCREMENTS
        self.fetch()
        self.PC = self.Pop()
        self.PC += 1
    def SEC(self): #SET CARRY
        self.fetch()
        self.SetSignal('C', True)
    def SED(self): #SET DECIMAL
        self.fetch()
        self.SetSignal('D', True)
    def SEI(self): #SET INTERRUPT DISABLE
        self.fetch()
        self.SetSignal('I', True) #DELAYED ONE INSTRUCTION! IMPLEMENT THIS!
    def STA(self): #STORE A. STORES ACC INTO MEMORY
        fetched = self.fetch()
        self.write(self.ACC, fetched)
    def STX(self): #STORE X. STORES X INTO MEMORY
        fetched =self.fetch()
        self.write(self.IXX, fetched)
    def STY(self): #STORE Y. STORES Y INTO MEMORY
        fetched = self.fetch()
        self.write(self.IXY, fetched)
    def TAX(self): #TRANSFER A TO X. X == ACC
        self.fetch()
        self.IXX = self.ACC
    def TAY(self): #TRANSFER A TO Y
        self.fetch()
        self.IXY = self.ACC
    def TSX(self): #TRANSFER STACK POINTER TO X
        self.fetch()
        self.IXX = self.SP
    def TXA(self): #TRANSFER X TO A
        self.fetch()
        self.ACC = self.IXX
    def TXS(self): #TRANSFER X TO SP
        self.fetch()
        self.SP = self.IXX
    def TYA(self): #TRANSFER Y TO A
        self.fetch()
        self.ACC = self.IXY