from pymtl import *

class sha1_w_mem( Model ):

    SHA1_ROUNDS = 79
    CTRL_IDLE   = 0
    CTRL_UPDATE = 1

    # Constructor
    def __init__( s ):

        s.reset_n = InPort(Bits(1))

        s.block = InPort (Bits(512))
        s.init  = InPort (Bits(1))
        s.next  = InPort (Bits(1))
        s.w     = OutPort(Bits(32))

        s.w_mem = [Wire(Bits(32)) for _ in range(16)]
        s.w_mem00_new = Wire(Bits(32))
        s.w_mem01_new = Wire(Bits(32))
        s.w_mem02_new = Wire(Bits(32))
        s.w_mem03_new = Wire(Bits(32))
        s.w_mem04_new = Wire(Bits(32))
        s.w_mem05_new = Wire(Bits(32))
        s.w_mem06_new = Wire(Bits(32))
        s.w_mem07_new = Wire(Bits(32))
        s.w_mem08_new = Wire(Bits(32))
        s.w_mem09_new = Wire(Bits(32))
        s.w_mem10_new = Wire(Bits(32))
        s.w_mem11_new = Wire(Bits(32))
        s.w_mem12_new = Wire(Bits(32))
        s.w_mem13_new = Wire(Bits(32))
        s.w_mem14_new = Wire(Bits(32))
        s.w_mem15_new = Wire(Bits(32))
        s.w_mem_we    = Wire(Bits(1))

        s.w_ctr_reg = Wire(Bits(7))
        s.w_ctr_new = Wire(Bits(7))
        s.w_ctr_we  = Wire(Bits(1))
        s.w_ctr_inc = Wire(Bits(1))
        s.w_ctr_rst = Wire(Bits(1))

        s.sha1_w_mem_ctrl_reg = Wire(Bits(1))
        s.sha1_w_mem_ctrl_new = Wire(Bits(1))
        s.sha1_w_mem_ctrl_we  = Wire(Bits(1))

        s.w_tmp = Wire(Bits(32))
        s.w_new = Wire(Bits(32))


        # Concurrent block
        @s.combinational
        def logic():
            s.w.value = s.w_tmp


        @s.tick
        def reg_update():

            if not s.reset_n:
                for ii in range(16):
                    s.w_mem[ii].value = 0

            else:
                if s.w_mem_we:
                    s.w_mem[0].next  = s.w_mem00_new
                    s.w_mem[1].next  = s.w_mem01_new
                    s.w_mem[2].next  = s.w_mem02_new
                    s.w_mem[3].next  = s.w_mem03_new
                    s.w_mem[4].next  = s.w_mem04_new
                    s.w_mem[5].next  = s.w_mem05_new
                    s.w_mem[6].next  = s.w_mem06_new
                    s.w_mem[7].next  = s.w_mem07_new
                    s.w_mem[8].next  = s.w_mem08_new
                    s.w_mem[9].next  = s.w_mem09_new
                    s.w_mem[10].next = s.w_mem10_new
                    s.w_mem[11].next = s.w_mem11_new
                    s.w_mem[12].next = s.w_mem12_new
                    s.w_mem[13].next = s.w_mem13_new
                    s.w_mem[14].next = s.w_mem14_new
                    s.w_mem[15].next = s.w_mem15_new

                if s.w_ctr_we:
                    s.w_ctr_reg.next = s.w_ctr_new

                if s.sha1_w_mem_ctrl_we:
                    s.sha1_w_mem_ctrl_reg.next = s.sha1_w_mem_ctrl_new


        @s.combinational
        def select_w():

            if s.w_ctr_reg < 16:
                s.w_tmp.value = s.w_mem[s.w_ctr_reg[0:4]]

            else:
                s.w_tmp.value = s.w_new


        @s.combinational
        def w_mem_update_logic():
            w_0  = Bits(32)
            w_2  = Bits(32)
            w_8  = Bits(32)
            w_13 = Bits(32)
            w_16 = Bits(32)

            s.w_mem00_new.value = 0
            s.w_mem01_new.value = 0
            s.w_mem02_new.value = 0
            s.w_mem03_new.value = 0
            s.w_mem04_new.value = 0
            s.w_mem05_new.value = 0
            s.w_mem06_new.value = 0
            s.w_mem07_new.value = 0
            s.w_mem08_new.value = 0
            s.w_mem09_new.value = 0
            s.w_mem10_new.value = 0
            s.w_mem11_new.value = 0
            s.w_mem12_new.value = 0
            s.w_mem13_new.value = 0
            s.w_mem14_new.value = 0
            s.w_mem15_new.value = 0

            w_0  = s.w_mem[0].value
            w_2  = s.w_mem[2].value
            w_8  = s.w_mem[8].value
            w_13 = s.w_mem[13].value
            w_16 = w_13 ^ w_8 ^ w_2 ^ w_0

            s.w_new.value = concat(w_16[0:31], w_16[31:32])

            if s.init:

                s.w_mem00_new.value = s.block[480 : 512]
                s.w_mem01_new.value = s.block[448 : 480]
                s.w_mem02_new.value = s.block[416 : 448]
                s.w_mem03_new.value = s.block[384 : 416]
                s.w_mem04_new.value = s.block[352 : 384]
                s.w_mem05_new.value = s.block[320 : 352]
                s.w_mem06_new.value = s.block[288 : 320]
                s.w_mem07_new.value = s.block[256 : 288]
                s.w_mem08_new.value = s.block[224 : 256]
                s.w_mem09_new.value = s.block[192 : 224]
                s.w_mem10_new.value = s.block[160 : 192]
                s.w_mem11_new.value = s.block[128 : 160]
                s.w_mem12_new.value = s.block[96  : 128]
                s.w_mem13_new.value = s.block[64  :  96]
                s.w_mem14_new.value = s.block[32  :  64]
                s.w_mem15_new.value = s.block[0   :  32]

            elif s.w_ctr_reg > 15:

                s.w_mem00_new.value = s.w_mem[1]
                s.w_mem01_new.value = s.w_mem[2]
                s.w_mem02_new.value = s.w_mem[3]
                s.w_mem03_new.value = s.w_mem[4]
                s.w_mem04_new.value = s.w_mem[5]
                s.w_mem05_new.value = s.w_mem[6]
                s.w_mem06_new.value = s.w_mem[7]
                s.w_mem07_new.value = s.w_mem[8]
                s.w_mem08_new.value = s.w_mem[9]
                s.w_mem09_new.value = s.w_mem[10]
                s.w_mem10_new.value = s.w_mem[11]
                s.w_mem11_new.value = s.w_mem[12]
                s.w_mem12_new.value = s.w_mem[13]
                s.w_mem13_new.value = s.w_mem[14]
                s.w_mem14_new.value = s.w_mem[15]
                s.w_mem15_new.value = s.w_new

                s.w_mem_we.value = 1

        @s.combinational
        def w_ctr():
            s.w_ctr_new.value = 0
            s.w_ctr_we.value = 0

            if s.w_ctr_rst:
                s.w_ctr_new.value = 0
                s.w_ctr_we.value = 1

            if s.w_ctr_inc:
                s.w_ctr_new.value = s.w_ctr_reg + 1
                s.w_ctr_we.value = 1


        @s.combinational
        def sha1_w_mem_fsm():
            s.w_ctr_rst.value = 0
            s.w_ctr_inc.value = 0
            s.sha1_w_mem_ctrl_new.value = CTRL_IDLE
            s.sha1_w_mem_ctrl_we.value = 0

            if s.sha1_w_mem_ctrl_reg == CTRL_IDLE:

                if s.init:
                    s.w_ctr_rst.value = 1
                    s.sha1_w_mem_ctrl_new.vlaue = CTRL_UPDATE
                    s.sha1_w_mem_ctrl_we.value = 1

            elif s.sha1_w_mem_ctrl_reg == CTRL_UPDATE:

                if s.next:
                    s.w_ctr_inc.value = 1

                if s.w_ctr_reg == SHA1_ROUNDS:
                    s.sha1_w_mem_ctrl_new.value = CTRL_IDLE
                    s.sha1_w_mem_ctrl_we.value = 1

















