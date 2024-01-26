
class Node:
    def __init__(self, elem):
        self.elem = elem
        self.nextNode = None
        self.prevNode = None

class Spisok:
    
    def __init__(self,size=100):
        self.box=[0]*size
        self.last=0
        
    def print_sp(self):
        if self.last == 0:
            print('Пусто', end=' ')
        else:
            for i in range(self.last):
                print(self.box[i], end='\t')
        print()
    
    def add_el(self,el):
        self.el = el
        if self.last==0:
            self.el.count += 1
            self.last+=1
            self.box[0]=el
        else:
            self.last += 1
            i = self.last
            while self.box[i] <= el and i>=0:
                i -= 1
                self.box[i+1] = self.box[i]
            self.box[i+1]=el
        
    def add_el_pos(self,pos,el):
        self.el = el
        if pos!=self.last:
            for i in range(self.last, pos,-1):
                self.box[i]=self.box[i-1]
            self.box[pos]=el
        else:
            self.box[self.last]=el
        self.last+=1

    
    def print_fe(self):
        if self.last == 0:
            print('tut pusto')
        else:
            for i in range(self.last):
                print(self.box[i-1], end='\n')
        print()
    
    def print_names(self):
        if self.last == 0:
            print("Инвентарь пуст...")
        else:
            for i in range(self.last, 0, -1):
                # print(self.box[i-1], end='\n')
                # print(self.box[i.el.name])
                print(self.box[i], self.el.name, self.el.count)
        print()
    
    def del_el(self,el):
        i = 0
        while self.box[i] != el and i < self.last:
            i += 1
        if i == self.last:
            print('net takogo')
        else:
            for j in range(i, self.last):
                self.box[j] = self.box[j+1]
            self.last -= 1
    ''' 
    def from_a_to_b(self,a,b):
        srez=upspis(100)
        for i in range(a,b+1):
            srez.add_el(self.box[i])
        return srez
    '''
    
    def poisk(self,el):
        i=0
        while self.box[i]!=el and i<self.last:
            i+=1
        if i==self.last: i=-1
        return i

class Spisok_Link: 

    def __init__(self):

        self._Start = None #Указывает всегда только на ПЕРВЫЙ элемент!
        self._End = None

    def Add_in_end(self, elem):

        new_ = Node(elem)
        
        if self._Start == None:
            self._Start = new_
            self._End = new_
        else:
            self._End.nextNode = new_
            self._End = new_
        
    def Add_in_begin(self, elem):

        new_ = Node(elem)

        if self._Start == None:
            self._Start = new_
            self._End = new_
        else:
            new_.nextNode = self._Start
            self._Start = new_
    
    def Kill_from_begin(self):
        
        node = None
        prev = None

        if self._Start == None:
            print("Spisok_Pust@")
        else:
            prev = self._Start
            self._Start = self._Start.nextNode
            return prev.elem

    def Kill(self, elem):
        
        p = self._Start
        prev = None

        if p == None:
            print("Spisok i tak pustoj!")

        else:
            while p != None:
                if p.elem != elem:
                    prev = p
                    p = p.nextNode
                else:
                    prev.nextNode = p.nextNode

    def add_between(self, elem, pos):
        
        new_ = Node(elem)

        p = self._Start
        prev = None

        counter = 0

        if p == None:
            self.Add_in_end(elem)
        else:
            if pos == 0:
                self.Add_in_begin(elem)
            else:
                while p != None and counter != pos:
                    counter += 1
                    prev = p
                    p = p.nextNode
                        
                else:
                    new_.nextNode = p
                    prev.nextNode = new_

    def poisk(self, elem):
        
        p = self._Start #Бегунок по всем узлам.
        
        if p == None:
            print("Тут уже пусто! Куда копаешь?")

        else:
            while p != None and p.elem != elem:
                p = p.nextNode

            return p

    def print_svjazi(self):
        if self._Start == None:
            print("Spisok Pust")

        elif self._Start != None and self._Previous == None:
                print("V spiske vsego odin element ->", self._Current.elem, "No dalee nichego net ->", self._Start.nextNode)

        elif self._Start != None and self._Next == None:
                print("V spiske vsego odin element ->", self._Current.elem, "No dalee nichego net ->", self._Start.nextNode)

        else:
            print("Start ->", self._Start.elem)
            print("Previous ->", self._Previous.elem, "Current ->", self._Current.elem, "Next ->", self._Current.nextNode)

    def print_spisok(self):
        
        p = self._Start #Бегунок по всем узлам.
        
        if p == None:
            print("Spisok pust")

        else:
            while p != None:
                print(p.elem)
                p = p.nextNode
            else:
                print("END")
    
    def count_check(self):
        
        counter = 0
        p = self._Start

        while p != None:
            counter += 1
            p = p.nextNode
        else:
            return counter

    def is_Empty(self) -> bool:
        if self._Start == None:
            return True
        else:
            return False

sp = Spisok_Link()

if __name__ == "__main__":
    #перебор элементов и взаимодействие с ними*
    
    sp.Add_in_begin(2)
    sp.Add_in_begin(5)
    sp.Add_in_begin(1)
    sp.Add_in_begin(4)
    sp.Add_in_begin(7)
    sp.Add_in_begin(12)
    sp.print_spisok()
    
    p = sp._Start

    for i in range(sp.count_check()):
       p.elem += 1
       p = p.nextNode
        
    sp.print_spisok()