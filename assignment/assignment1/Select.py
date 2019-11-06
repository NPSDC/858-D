class Select(object):
    def __init__(self, r_ob):
        if(type(r_ob).__name__ != 'Rank'):
            raise Exception("object does not belong to Rank")
        self.rank_ob = r_ob
        self.max_rank = r_ob.rank1(r_ob.get_length() - 1)
    
    def get_rank_ob(self):
        return self.rank_ob
    
    def get_max_rank(self):
        return self.max_rank
    
    def select1(self, i):
        r_ob = self.get_rank_ob()
        start = 0
        end = r_ob.get_length() - 1
        
       # if(i > self.get_max_rank()):
        #        return -1

        while start <= end:
            mid = (start + end)//2
            if(i == r_ob.rank1(mid)):
                for ind in range(start, mid+1):
                    if(i == r_ob.rank1(ind)):
                        return ind
                
    #
            if(i > r_ob.rank1(mid)):
                start = mid + 1
            if(i < r_ob.rank1(mid)):
               end = mid - 1            
           # break
        return -1

    def select0(self, i):
        r_ob = self.get_rank_ob()
        start = 0
        end = r_ob.get_length() - 1
        
       # if(i > self.get_max_rank()):
        #        return -1

        while start <= end:
            mid = (start + end)//2
            if(i == r_ob.rank0(mid)):
                for ind in range(start, mid+1):
                    if(i == r_ob.rank0(ind)):
                        return ind
#                return(mid)
            if(i > r_ob.rank0(mid)):
                start = mid + 1
            if(i < r_ob.rank0(mid)):
               end = mid - 1            
           # break
        return -1