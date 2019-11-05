import sys
import BitVector as BV
import math

class Rank(object):
    def __init__(self, b):
        self.b_vec = b
        self.length = b.length()
        self.block_size, self.super_block_size = self.__get_size__(b)
        self.lk_table, self.block_table, self.super_block_table = self.__create_structure__()
    
    def __get_size__(self, b):
        log_2_b = math.log2(b.length())
       # print(log_2_b)
        block_size = math.ceil(log_2_b/2)
        super_block_size = int(log_2_b*log_2_b//2)
        super_block_size = (super_block_size//block_size)*block_size
     #   print(block_size, super_block_size)
        return(block_size, super_block_size)
        
    def get_bit_vector(self):
        return self.b_vec
    
    def get_block_size(self):
        return self.block_size
    
    def get_super_block_size(self):
        return self.super_block_size
    
    def get_lk_table(self):
        return self.lk_table
    
    def get_b_table(self):
        return self.block_table
    
    def get_s_b_table(self):
        return self.super_block_table
    
    def get_length(self):
        return self.length
    
    @classmethod    
    def add_num(cls, b_vec, num = 1, to_int = False):
        l = b_vec.length()
        zero_bv = BV.BitVector(bitstring = '0')
        for n in range(num):
            i = l-1
            while(b_vec[i] != 0):
                b_vec[i:i+1] = ~b_vec[i:i+1]
                i = i - 1
            b_vec[i:i+1] = ~b_vec[i:i+1]
        
        if(to_int):
            print(b_vec.int_val())
        
        
    def empty_block(self, size):
        return(BV.BitVector(size = size))
    
    def create_substrings(self, b, i, n, vals):
        if(i == n):
            vals.append(b[:])
            return
        b[i] = 0
        self.create_substrings(b, i+1, n, vals)
        b[i] = 1
        self.create_substrings(b, i+1, n, vals)
    
    def create_lookup_mat(self, b_size, b_bits):
        vals = []
        b = [0]*b_size
        self.create_substrings(b, 0, b_size, vals)
        inn_block = []

        for i in range(len(vals)):
            inn_block.append(list())
            for j in range(b_size):
                inn_block[i].append(self.empty_block(b_bits))
                if(j != 0):
                    Rank.add_num(inn_block[i][j], num = inn_block[i][j-1].int_val() + vals[i][j])
                else:
                    Rank.add_num(inn_block[i][j], num = vals[i][j])
                
        return(inn_block)
        
    def __create_structure__(self, pad = True):
        b_vec = self.get_bit_vector()
        b_size = self.get_block_size()
        s_b_size = self.get_super_block_size()
        n = b_vec.length()
        
        # if(pad):
        #     rem = b_vec.length() % s_b_size
        #     if(rem != 0):
        #         bits_add = s_b_size - rem
        #         b_vec += self.empty_block(size = bits_add)
                
      #  n_super_blocks = math.ceil(b_vec.length()/s_b_size)
      #  n_blocks = s_b_size/b_size
        
        b_list = list()
        s_b_list = list()
        s = 0 ##tracker of superblock
        b = 0 ##tracker of block
        
        s_b_bits = math.ceil(math.log2(n))
        b_bits = math.ceil(math.log2(s_b_size))
        l_b_bits = math.ceil(math.log2(math.log2(n)))
        
        b_list.append(list())
        b_list[s].append(self.empty_block(b_bits))
        s_b_list.append(self.empty_block(s_b_bits))
        
        lup_tab = self.create_lookup_mat(b_size, l_b_bits)
        
        for i in range(b_size, len(b_vec), b_size):
            if(i%s_b_size == 0):
                s_b_list.append(self.empty_block(s_b_bits))
                s_b_list[s + 1] = s_b_list[s][:]
                Rank.add_num(s_b_list[s + 1], b_list[s][b].int_val() + 
                                         lup_tab[b_vec[(i-b_size):i].int_val()][b_size-1].int_val())
                s += 1
                b = 0
                b_list.append(list())
                b_list[s].append(self.empty_block(b_bits))
                
            elif(i%b_size == 0):
                b_list[s].append(self.empty_block(b_bits))
                b_list[s][b+1] = b_list[s][b][:]
                Rank.add_num(b_list[s][b+1], lup_tab[b_vec[(i-b_size):i].int_val()][b_size-1].int_val())
               # print(b_list[s][b+1].int_val(), lup_tab[b_vec[(i-b_size):i].int_val()][b_size-1].int_val())
                b = b + 1
            
        return lup_tab, b_list, s_b_list

    def rank1(self, i):
        if(i >= self.get_length()):
            raise Exception("i exceeds length of bit vector")
        lk = self.get_lk_table()
        sbt = self.get_s_b_table()
        bt = self.get_b_table()
        b_size = len(lk[0])
        b_vec = self.get_bit_vector()
        
        s = i//self.get_super_block_size()
        b = (i%self.get_super_block_size())//self.get_block_size()
        lk_bit = (i%self.get_super_block_size())%self.get_block_size()

        lk_ind = i-lk_bit+b_size
        if(lk_ind < b_vec.length()):
            r_lk = lk[b_vec[(i-lk_bit):lk_ind].int_val()][lk_bit].int_val()
        else:
            not_allowed = lk_ind - b_vec.length()
            bv_req = b_vec[(i-lk_bit):b_vec.length()] + self.empty_block(not_allowed)
            r_lk = lk[bv_req.int_val()][lk_bit].int_val()
        return(sbt[s].int_val() + bt[s][b].int_val() + r_lk)
        #return(sbt[s].int_val() + bt[b].int_val() + lk[self.b_vec[i-lk_bit]])
    
    def rank0(self, i):
        return i + 1 - self.rank1(i)
    
    def overhead(self):
        lk = self.get_lk_table()
        sbt = self.get_s_b_table()
        bt = self.get_b_table()
        bv = self.get_bit_vector()

        s_b_bits = len(sbt)*sbt[0].length()
        bt_bits = len(bt)*len(bt[0])*bt[0][0].length()
        lk_bits = len(lk)*len(lk[0])*lk[0][0].length()
        return(s_b_bits + bt_bits + lk_bits + bv.length())
            
    