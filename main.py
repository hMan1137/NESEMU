import time
#THE 6502 BEING LITTLE ENDIAN--AND FULL BEING 2 BYTE--MEMORY ADDRESSES NEED TO BE ASSEMBLED IN THE CORRECT ORDER WITH THIS FUNCTION
def AssembleByte(low, high):
    return (high << 8) | low


#HERES A GIGANTIC DICTIONARY LOOKUP THAT'S GONNA COME IN HANDY LATER
#IT STORES IN THE FOLLOWING PATTERN: 'OPCODE: ['NAME OF INSTRUCTION', 'ADDRESSING MODE USED', NUMBER OF BYTES USED BY INSTRUCTION, LEAST NUMBER OF CLOCK CYCLES USED]'

class _6502:



    def __init__(self):
        #THE NES USES A RESET VECTOR, SO WE'RE INITIALISING AS IF HAVING JUST DONE A RESET
        self.operations = {
            0x69: [self.ADC, self.IMM, 2, 2], 0x65: [self.ADC, self.ZP0, 2, 3], 0x75: [self.ADC, self.ZPX, 2, 4], 0x6D: [self.ADC, self.ABS, 3, 4],
            0x7D: [self.ADC, self.ABX, 3, 4], 0x79: [self.ADC, self.ABY, 3, 4], 0x61: [self.ADC, self.IZX, 2, 6], 0x71: [self.ADC, self.IZY, 2, 5],
            0x29: [self.AND, self.IMM, 2, 2], 0x25: [self.AND, self.ZP0, 2, 3], 0x35: [self.AND, self.ZPX, 2, 4], 0x2D: [self.AND, self.ABS, 3, 4],
            0x3D: [self.AND, self.ABX, 3, 4], 0x39: [self.AND, self.ABY, 3, 4], 0x21: [self.AND, self.IZX, 2, 6], 0x31: [self.AND, self.IZY, 2, 5],
            0x0A: [self.ASL, self.AC1, 1, 2], 0x06: [self.ASL, self.ZP0, 2, 5], 0x16: [self.ASL, self.ZPX, 2, 6], 0x0E: [self.ASL, self.ABS, 3, 6],
            0x1E: [self.ASL, self.ABX, 3, 7], 0x90: [self.BCC, self.REL, 2, 2], 0xB0: [self.BCS, self.REL, 2, 2], 0xF0: [self.BEQ, self.REL, 2, 2],
            0x24: [self.BIT, self.ZP0, 2, 3], 0x2C: [self.BIT, self.ABS, 3, 4], 0x30: [self.BMI, self.REL, 2, 2], 0xD0: [self.BNE, self.REL, 2, 2],
            0x10: [self.BPL, self.REL, 2, 2], 0x00: [self.BRK, self.IMM, 2, 7], 0x50: [self.BVC, self.REL, 2, 2], 0x70: [self.BVS, self.REL, 2, 2],
            0x18: [self.CLC, self.IMP, 1, 2], 0xD8: [self.CLD, self.IMP, 1, 2], 0x58: [self.CLI, self.IMP, 1, 2], 0xB8: [self.CLV, self.IMP, 1, 2],
            0xC9: [self.CMP, self.IMM, 2, 2], 0xC5: [self.CMP, self.ZP0, 2, 3], 0xD5: [self.CMP, self.ZPX, 2, 4], 0xCD: [self.CMP, self.ABS, 3, 4],
            0xDD: [self.CMP, self.ABX, 3, 4], 0xD9: [self.CMP, self.ABY, 3, 4], 0xC1: [self.CMP, self.IZX, 2, 6], 0xD1: [self.CMP, self.IZY, 2, 5],
            0xE0: [self.CPX, self.IMM, 2, 2], 0xE4: [self.CPX, self.ZP0, 2, 3], 0xEC: [self.CPX, self.ABS, 3, 4], 0xC0: [self.CPY, self.IMM, 2, 2],
            0xC4: [self.CPY, self.ZP0, 2, 3], 0xCC: [self.CPY, self.ABS, 3, 4], 0xC6: [self.DEC, self.ZP0, 2, 5], 0xD6: [self.DEC, self.ZPX, 2, 6],
            0xCE: [self.DEC, self.ABS, 2, 6], 0xDE: [self.DEC, self.ABY, 2, 7], 0xCA: [self.DEX, self.IMP, 1, 2], 0x88: [self.DEY, self.IMP, 1, 2],
            0x49: [self.EOR, self.IMM, 2, 2], 0x45: [self.EOR, self.ZP0, 2, 3], 0x55: [self.EOR, self.ZPX, 2, 4], 0x4D: [self.EOR, self.ABS, 3, 4],
            0x5D: [self.EOR, self.ABX, 3, 4], 0x59: [self.EOR, self.ABY, 3, 4], 0x41: [self.EOR, self.IZX, 2, 6], 0x51: [self.EOR, self.IZY, 2, 5],
            0xE6: [self.INC, self.ZP0, 2, 5], 0xF6: [self.INC, self.ZPX, 2, 6], 0xEE: [self.INC, self.ABS, 3, 6], 0xFE: [self.INC, self.ABX, 3, 7],
            0xE8: [self.INX, self.IMP, 1, 2], 0xC8: [self.INY, self.IMP, 1, 2], 0x4C: [self.JMP, self.ABS, 3, 3], 0x6C: [self.JMP, self.IND, 3, 5],
            0x20: [self.JSR, self.ABS, 3, 6], 0xA9: [self.LDA, self.IMM, 2, 2], 0xA5: [self.LDA, self.ZP0, 2, 3], 0xB5: [self.LDA, self.ZPX, 2, 4],
            0xAD: [self.LDA, self.ABS, 3, 4], 0xBD: [self.LDA, self.ABX, 3, 4], 0xB9: [self.LDA, self.ABY, 3, 4], 0xA1: [self.LDA, self.IZX, 2, 6],
            0xB1: [self.LDA, self.IZY, 2, 5], 0xA2: [self.LDX, self.IMM, 2, 2], 0xA6: [self.LDX, self.ZP0, 2, 3], 0xB6: [self.LDX, self.ZPY, 2, 4],
            0xAE: [self.LDX, self.ABS, 3, 4], 0xBE: [self.LDX, self.ABY, 3, 4], 0xA0: [self.LDY, self.IMM, 2, 2], 0xA4: [self.LDY, self.ZP0, 2, 3],
            0xB4: [self.LDY, self.ZPX, 2, 4], 0xAC: [self.LDY, self.ABS, 3, 4], 0xBC: [self.LDY, self.ABX, 3, 4], 0x4A: [self.LSR, self.AC1, 1, 2],
            0x46: [self.LSR, self.ZP0, 2, 5], 0x56: [self.LSR, self.ZPX, 2, 6], 0x4E: [self.LSR, self.ABS, 3, 6], 0x5E: [self.LSR, self.ABX, 3, 7],
            0xEA: [self.NOP, self.IMP, 1, 2], 0x09: [self.ORA, self.IMM, 2, 2], 0x05: [self.ORA, self.ZP0, 2, 3], 0x15: [self.ORA, self.ZPX, 2, 4],
            0x0D: [self.ORA, self.ABS, 3, 4], 0x1D: [self.ORA, self.ABX, 3, 4], 0x19: [self.ORA, self.ABY, 3, 4], 0x01: [self.ORA, self.IZX, 2, 6],
            0x11: [self.ORA, self.IZY, 2, 5], 0x48: [self.PHA, self.IMP, 1, 3], 0x08: [self.PHP, self.IMP, 1, 3], 0x68: [self.PLA, self.IMP, 1, 4],
            0x28: [self.PLP, self.IMP, 1, 4], 0x2A: [self.ROL, self.AC1, 1, 2], 0x26: [self.ROL, self.ZP0, 2, 5], 0x36: [self.ROL, self.ZPX, 2, 6],
            0x2E: [self.ROL, self.ABS, 3, 6], 0x3E: [self.ROL, self.ABX, 3, 7], 0x6A: [self.ROR, self.AC1, 1, 2], 0x66: [self.ROR, self.ZP0, 2, 5],
            0x76: [self.ROR, self.ZPX, 2, 6], 0x6E: [self.ROR, self.ABS, 3, 6], 0x7E: [self.ROR, self.ABX, 3, 7], 0x40: [self.RTI, self.IMP, 1, 6],
            0x60: [self.RTS, self.IMP, 1, 6], 0xE9: [self.SBC, self.IMM, 2, 2], 0xE5: [self.SBC, self.ZP0, 2, 3], 0xF5: [self.SBC, self.ZPX, 2, 4],
            0xED: [self.SBC, self.ABS, 3, 4], 0xFD: [self.SBC, self.ABX, 3, 4], 0xF9: [self.SBC, self.ABY, 3, 4], 0xE1: [self.SBC, self.IZX, 2, 6],
            0xF1: [self.SBC, self.IZY, 2, 5], 0x38: [self.SEC, self.IMP, 1, 2], 0xF8: [self.SED, self.IMP, 1, 2], 0x78: [self.SEI, self.IMP, 1, 2],
            0x85: [self.STA, self.ZP0, 2, 3], 0x95: [self.STA, self.ZPX, 2, 4], 0x8D: [self.STA, self.ABS, 3, 4], 0x9D: [self.STA, self.ABX, 3, 5],
            0x99: [self.STA, self.ABY, 3, 5], 0x81: [self.STA, self.IZX, 2, 6], 0x91: [self.STA, self.IZY, 2, 6], 0x86: [self.STX, self.ZP0, 2, 3],
            0x96: [self.STX, self.ZPX, 2, 4], 0x8E: [self.STX, self.ABS, 3, 4], 0x84: [self.STY, self.ZP0, 2, 3], 0x94: [self.STY, self.ZPX, 2, 4],
            0x8C: [self.STY, self.ABS, 3, 4], 0xAA: [self.TAX, self.IMP, 1, 2], 0xA8: [self.TAY, self.IMP, 1, 2], 0xBA: [self.TSX, self.IMP, 1, 2],
            0x8A: [self.TXA, self.IMP, 1, 2], 0x9A: [self.TXS, self.IMP, 1, 2], 0x98: [self.TYA, self.IMP, 1, 2],
        }

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
        with open("6502_functional_test.bin", "rb") as f:
            self.RAM[:] = f.read() #setting RAM to a specific test ROM for testing purposes
        self.PC = AssembleByte(self.RAM[0xFFFC], self.RAM[0xFFFD]) #THIS IS WHERE THE RESET POSITION FOR THE PC IS LOCATED. USUALLY IT'S EQUAL TO 0x8000 BUT ITS MORE...
        #...INTELLIGENT TO MATHEMATICALLY CALCULATE IT LIKE THE 6502 DID SINCE ITS NOT ACTUALLY A HARD-CODED THING, SO THERE COULD BE A WEIRD CASE WHERE IT DOES NOT...
        #...RESET TO 0x8000
        self.PC = 0x0400 #REQUIRED FOR THIS TEST ROM SPECIFICALLY
        self.cycle = 0 #A VARIABLE COUNTING DOWN ON THE NUMBER OF CLOCK CYCLES LEFT ON AN INSTRUCTION. NEEDED TO KNOW WHEN IT CAN LEGALLY MOVE ON TO THE NEXT INSTRUCTION
        self.AddCycle = [0, 0] #WILL ADD A CYCLE IF BOTH ELEMENTS ARE ONE. ADDRESSING MODE WILL TURN ON THE FIRST ELEMENT, THE INSTRUCTION WILL TURN ON THE SECOND
        self.AddrModes = {'IMP':self.IMP, 'IMM':self.IMM, 'ABS':self.ABS, 'ABX':self.ABX, 'ABY':self.ABY, 'IZX':self.IZX, 'IZY':self.IZY, 'REL':self.REL,
                          'ZP0': self.ZP0, 'ZPX':self.ZPX, 'ZPY': self.ZPY}
        self.JumpAddress = 0 #jump needs special treatment in ABS mode
        #self.Instructions = {'ADC': self.ADC, 'SBC': self.SBC, 'AND': self.AND, 'ASL': self.ASL, 'BCC':self.BCC, 'BCS':self.BCS, 'BEQ': self.BEQ, 'BIT': self.BIT,
         #                    'BMI': self.BMI, 'BNE':self.BNE, 'BPL': self.BPL, 'BRK': self.BRK, 'BVC': self.BVC, 'BVS': self.BVS, 'CRC': self.CLC, 'CLD': self.CLD
    #A DETERMINER FUNCTION FOR KNOWING WHAT ADDRESS MODE WE'RE WORKING WITH AND THUS PERFORMING THE APPROPRIATE ADDRESSING MODE FUNCTION. THE ADDRESSING MODES ARE DEALT WITH...
    #...A LITTLE LATER
    #def UseMode(self, mode):
     #   if mode == 'ACC': #some commands address the accumulator directly, so we're gonna deal with that separately here
      #      return -1
      #  elif mode != 'ACC' & mode not in list(self.AddrModes.keys()): #CATCH ALL FOR ILLEGAL ADDRESSING MODES
      #      return -2
      #  else:
      #      return self.AddrModes[mode]()
    #FUNCTIONS THAT READ FROM AND WRITE TO THE ADDRESS

    def read(self, mode):
        address = mode()
        if mode == self.REL: # or mode == self.ABS or mode == self.ABX or mode == self.ABY or mode == self.ZP0 or mode == self.ZPX or mode == self.ZPY:
            print("heyup")
            self.addr = address
        else:
            self.addr = self.ACC if address == -1 else self.RAM[address]

        #self.PC += 1
        self.JumpAddress = address
        return address #RETURNING THE INDEX OF RAM WE CHECK AT FOR THE SAKE OF WRITING CHANGES DIRECTLY TO MEMORY
    def write(self, data, address, x = False, y = False):
       # Mode = self.UseMode(mode)
       if True:
           if x:
               self.IXX = data
               self.IXX &= 0xFF
           if y:
               self.IXY = data
               self.IXY &= 0xFF
       if address== -1:
           self.ACC = data
           self.ACC &= 0xFF

       else:
           self.RAM[address] = data & 0xFF
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
    def AC1(self):
        return -1
    def IMM(self):
        val = self.PC
        self.PC += 1
        #IMMEDIATE ADDRESSING, THE OPERAND IS THE NEXT BYTE
        return val
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
        val = AssembleByte(self.GetByte(), self.GetByte())
        if (val + self.IXX) & 0xFF < val:
            self.AddCycle[0] = 1 #PAGE BOUNDARY HAS BEEN CROSSED
        return val + self.IXX

    def ABY(self): #ABSOLUTE ADDRESSING WITH A Y REGISTER OFFSET
        val = AssembleByte(self.GetByte(), self.GetByte())
        if (val + self.IXY) & 0xFF < val:
            self.AddCycle[0] = 1 #PAGE BOUNDARY HAS BEEN CROSSED
        return val + self.IXY

    def IZX(self): #INDIRECT ZERO-PAGE ADDRESSING WITH X REGISTER OFFSET
        return self.ZeroPage(self.GetByte() + self.IXX)

    def IZY(self): #SAME THING WITH Y-OFFSET, EXCEPT ITS ACTUALLY THE FINAL ADDRESS THATS OFFSET FOR SOME REASON
        var = self.ZeroPage(self.GetByte())
        if (var + self.IXY) & 0xFF < var:
            self.AddCycle[0] = 1  #PAGE BOUNDARY HAS BEEN CROSSED
        return var + self.IXY

    def REL(self): #THIS ONES WEIRD...IT BASICALLY TAKES THE ADDRESS POINTED TO BY THE PC AND TURNS IT INTO A SIGNED OFFSET BETWEEN -128 AND 127
        #ALL WE NEED TO RETURN HERE IS THE BYTE CONVERTED TO SIGNED
       # if self.GetByte(1) & 0x80: #AND WITH BINARY 10000000, so we're basically checking if the number is 128 or bigger
            val =self.GetByte()
            print("hiiiii")
            self.AddCycle[0] = 1
            #if val & 0x80:
             #   val |= 0xFF00

            return val - 0x100 if val & 0x80 else val #SUBTRACT 256 TO MAKE IT WRAP TO NEGATIVE

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
        Mode = self.operations[opcode][1]

        return self.read(Mode) #NOW THAT WE HAVE THE MODE, WE RUN IT THROUGH READ TO SET SELF.ADDR TO THE OPERAND, THIS RETURNS THE RETURN INDEX OF INSTRUCTION
   # def start(self): #A METHOD TO CALL WHEN STARTING THE EXECUTION OF AN INSTRUCTION.
    #    opcode = self.RAM[self.PC]
     #   if opcode not in list(self.operations.keys()):
         #   self.PC += 1
      #      return
       # else:
        #    (self.operations[opcode][0]())

    def clock(self):

        print("hi")
        if self.cycle == 0:
            opcode = self.RAM[self.PC]  # A FUNCTION TELLING THE CPU THAT ONE CLOCK CYCLE HAS PASSED. THIS IS THE HEART OF PROGRAM EXECUTION
            self.cycle = self.operations[opcode][3]
            #HANDLE ADDITIONAL CLOCK CYCLES:
            start = self.operations[opcode][0]() #START PC EXECUTION, OPCODE ZERO STORES THE INSTRUCTION
            if self.AddCycle[0] == 1:
                if self.AddCycle[1] == 1:
                    self.cycle += 1
                elif self.AddCycle[1] > 1:
                    self.cycle += 2
            self.AddCycle = [0, 0]
            #LIMIT TO ONCE PER CYCLE FOR TESTING

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
        val =self.RAM[self.SP | 0x100]
        #self.SP += 1
        return val

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
        self.SetSignal('N', val & 0x80 != 0)

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
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def SBC(self): #SUBTRACT WITH BORROW, C, V, N, Z
        #BORROW EFFECTIVELY MEANS NOT(CARRY)

        self.fetch()
        base = self.ACC - self.addr
        val = base - (1-self.Flag['C'])
        self.ACC = val & 0x00FF
        self.SetSignal('C', val > 0x0000) #IT COULD NEVER REACH THE UPPER LIMIT OF 255, SO HERE A CARRY OCCURS WHEN IT REACHES THE LOWER LIMIT OF 0
        self.SetSignal('Z', val & 0x00FF == 0)
        self.SetSignal('N', val & 0x80 != 0)
        self.SetSignal('V', 0x0080 & ((self.ACC ^ self.addr) & ((self.ACC & self.addr) ^ val))) #HERE, IT IS THE SAME EXCEPT THE NOT FROM THE XOR IS REMOVED BECAUSE...
        #...OVERFLOW IN SUBTRACTION CAN ONLY OCCUR WHEN BOTH NUMBERS HAVE *DIFFERENT* MSBs, WHICH IS BECAUSE SUBTRACTING A FROM B IS THE SAME THING AS ADDING THE...
        #...COMPLEMENT OF A FROM B. SO, SUBTRACTING DIFFERENT MSBs BECOMES THE SAME AS ADDING THE SAME MSBs
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def AND(self): #BITWISE AND. Z, N
        self.fetch()
        self.ACC = self.ACC & self.addr & 0xFF
        self.SetSignal('N', self.ACC & 0x80 != 0)
        self.SetSignal('Z', self.ACC & 0x00FF == 0)
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def ASL(self): #ARITHMETIC LEFT SHIFT TO EITHER ACC OR VALUE. C, Z, N
        mode = self.fetch()
        if mode == self.ACC:
            #THE CARRY IS SET IF THE INITIAL VALUE HAD BIT 7 ON
            self.SetSignal('C', self.ACC & 0x80 != 0)
            self.ACC = self.ACC << 1
            #THE NEGATIVE IS SET IF THE NEW BIT-SHIFTED VALUE HAS BIT 7 ON
            self.SetSignal('N', self.ACC & 0x80 != 0)

        else:
            self.SetSignal('C', self.addr & 0x80 != 0)
            self.addr = self.addr << 1
            self.SetSignal('N', self.addr & 0x80 != 0)
            self.write(self.addr, mode)
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
        self.SetSignal('Z', (self.ACC & self.addr) == 0)
        self.SetSignal('N', (self.addr & 0x0080) == 1)
        self.SetSignal('V', (self.addr & 0x0040) == 1)
    def BMI(self): #BRANCH IF MINUS. SAME AS THE PREVIOUS BRANCHES FOR THE NEGATIVE FLAG
        self.fetch()
        if self.Flag['N']:
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            self.PC += self.addr
    def BNE(self): #BRANCH IF NOT EQUAL. (THE ZERO FLAG IS CLEAR)
        self.fetch()
        #print("hiiiiiiiiiiiiiii")
        if not self.Flag['Z']:
           # print("heyyyyy")
            self.AddCycle[1] = 1  # ADDS A CYCLE IF BRANCH IS FULL
            if (self.PC + self.addr) & 0xFF < self.PC: #A PAGE BOUNDARY HAS BEEN CROSSED
                self.AddCycle[1] = 2 #ADDS TWO CYCLES INSTEAD
            print(self.PC)
            self.PC += self.addr
            print(self.PC)

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
        self.PC = AssembleByte(self.RAM[0xFFFE], self.RAM[0xFFFF])
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
        val = (self.ACC - self.addr) & 0xFF
        print(val)

        self.SetSignal('Z', val == 0)
        self.SetSignal('N', val & 0x80 != 0)
        self.SetSignal('C', not self.Flag['N'])
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def CPX(self): #COMPARE X. SAME THING WITH REGISTER X. C, Z, N
        self.fetch()
        val = (self.IXX - self.addr) & 0xFF
       # self.SetSignal('C', val & 0x80 >= 0)
        self.SetSignal('Z', val == 0)
        self.SetSignal('N', val &0x80 != 0)
        self.SetSignal('C', not self.Flag['N'])
    def CPY(self): #COMPARE Y. SAME THING WITH REGISTER Y. C, Z, N
        self.fetch()
        val = (self.IXY - self.addr) & 0xFF
        #self.SetSignal('C', val & 0x80 >= 0)
        self.SetSignal('Z', val == 0)
        self.SetSignal('N', val & 0x80 != 0)
        self.SetSignal('C', not self.Flag['N'])
    def DEC(self):#DECREMENT MEMORY. SUBTRACT ONE FROM A MEMORY LOCATION. WRITES BACK TO MEMORY/ ACC.Z. N

        fetched = self.fetch()
        self.write((self.addr - 1), fetched)
        self.SetSignal('Z', (self.addr - 1) & 0xFF == 0)
        self.SetSignal('N', ((self.addr - 1) & 0xFF & 0x80 != 0))
    def DEX(self): #DECREMENT X. SAME THING BUT FOR THE X REGISTER. Z, N
        self.fetch()
        self.IXX -= 1
        self.IXX &= 0xFF
        self.SetSignal('Z', self.IXX== 0)
        self.SetSignal('N', (self.IXX & 0x80 != 0))
    def DEY(self): #DECREMENT Y. SAME THING BUT FOR THE Y REGISTER. Z, N
        self.fetch()
        self.IXY -= 1
        self.IXY &= 0xFF
        self.SetSignal('Z', self.IXY== 0)
        self.SetSignal('N', (self.IXY & 0x80 != 0))
    def EOR(self): #EXCLUSIVE OR. EORs BETWEEN ACC AND ADDR, SETTING REGISTERS APPROPRIATELY. Z,N.
        self.fetch()
        self.ACC = self.ACC ^ self.addr
        self.SetSignal('Z', self.ACC == 0)
        self.SetSignal('N', self.ACC &0x80 !=0)
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def INC(self): #INCREMENT MEMORY. ADD ONE TO A MEMORY LOCATION. WRITES BACK TO MEMORY/ ACC. Z, N.
        fetched = self.fetch()
        self.write((self.addr + 1), fetched)
        self.SetSignal('Z', self.addr +1 == 0)
        self.SetSignal('N', ((self.addr+ 1) & 0xFF & 0x80!= 0))
    def INX(self): #INCREMENT X. SAME THING BUT FOR THE X REGISTER. Z, N.
        self.fetch()
        self.IXX += 1
        self.IXX &= 0xFF
        self.SetSignal('Z', self.IXX == 0)
        self.SetSignal('N', (self.IXX & 0x80 != 0))

    def INY(self):  # DECREMENT Y. SAME THING BUT FOR THE Y REGISTER. Z, N
        self.fetch()
        self.IXY += 1
        self.IXX &= 0xFF
        self.SetSignal('Z', self.IXY == 0)
        self.SetSignal('N', (self.IXY & 0x80 != 0))

    def JMP(self): #JUMP. PROGRAM COUNTER IS EQUAL TO THE SELF.ADDR.
        self.fetch()
        self.PC = self.JumpAddress
    def JSR(self): #JUMP TO SUBROUTINE. PUSHES CURRENT PC TO STACK THEN SETS IT TO SELF.ADDR. USED WHEN YOU WANT TO BE ABLE TO GO BACK FROM WHERE YOU JUMPED.
        self.fetch()
        self.Push((self.PC>> 8)& 0xFF)
        self.Push(self.PC & 0xFF)
        self.PC = self.JumpAddress
    def LDA(self): #LOAD A. LOADS SELF.ADDR INTO ACC. Z, N.
        self.fetch()
        self.ACC = self.addr
        self.SetSignal('Z', self.ACC == 0)
        self.SetSignal('N', self.ACC & 0x80 !=0)
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def LDX(self): #LOAD Y. LOADS SELF.ADDR INTO Y. Z, N.
        fetched = self.fetch()
        self.write(self.addr,fetched, True)
        self.SetSignal('Z', self.IXX == 0)
        self.SetSignal('N', self.IXX & 0x80 !=0)
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABY
    def LDY(self): #LOAD Y. LOADS SELF.ADDR INTO Y. Z, N.
        fetched =self.fetch()
        self.write(self.addr, fetched, False, True)
        self.SetSignal('Z', self.IXY == 0)
        self.SetSignal('N', self.IXY &0x80 != 0)
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX
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
        self.AddCycle[1] = 1 #JUST LETTING THE CLOCK KNOW ABOUT POTENTIAL ADDITIONAL CYCLES ON ABX, ABY AND IZY
    def PHA(self): #PUSH A. SIMPLY PUSHES ACC TO THE STACK
        self.fetch()
        self.Push(self.ACC)
    def PHP(self): #PUSH PROCESSOR STATUS. PUSHES THE STATUS FLAGS AND PUSHES B AS 1. B
        self.fetch()
        self.SetSignal('B', True)
        self.SetSignal(1, True)
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
        low = self.Pop()
        high = self.Pop()

        self.PC = AssembleByte(low, high)#HIGH BYTE COMES IN SECOND, SO IT NEEDS TO BE ASSEMBLED CORRECTLY
    def RTS(self): #RETURN FROM SUBROUTINE. POPS ADDRESS FROM STACK INTO PC, THEN INCREMENTS
        self.fetch()
        low = self.Pop()
        high = self.Pop()
        self.PC = AssembleByte(low, high)
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
    def STA(self):
        print("eeeee")#STORE A. STORES ACC INTO MEMORY
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
cpu = _6502()
cpu.PC = 0x0400
while True:


    #print(hex(cpu.ACC), hex(cpu.IXX), hex(cpu.IXY), hex(cpu.SP), hex(cpu.addr), hex(cpu.PC), hex(cpu.RAM[cpu.PC+1]), hex(cpu.RAM[(cpu.PC)]), hex(cpu.RAM[cpu.PC+2]))
    cpu.clock()
    print(hex(cpu.ACC), hex(cpu.IXX), hex(cpu.IXY), hex(cpu.SP), hex(cpu.addr), hex(cpu.PC), hex(cpu.RAM[(cpu.PC) & 0xFFFF]), hex(cpu.RAM[(cpu.PC+1) & 0xFFFF]), hex(cpu.RAM[(cpu.PC+2) & 0xFFFF]))
    print(cpu.Flag)
  #  if cpu.PC == 0x674:
   #     break

    #time.sleep(0.00001)