class Message:
    def __init__(self, msg):
        self.msg = msg
        self.char = []
        self.prob_list = []

    def get_data(self):
        self.prob(self.msg)
        self.char, self.prob_list = self.sort(self.char, self.prob_list)
        
        return self.char, self.prob_list

    def prob(self, msg):      
        for i in range(len(msg)):
            if self.repeat_check(msg, i):
                continue
            else:
                self.char.append(msg[i])      
                self.prob_list.append(msg.count(msg[i])/len(msg))

    def repeat_check(self, msg, symbol_number):
        for i in range(symbol_number):
            if msg[i] == msg[symbol_number]:
                return True #Symbol repeats

        return False #Symbol does not repeat

    def sort(self, chars, probs):
        sorted_p = probs[:]
        sorted_p.sort()
        sorted_c = []

        for i in range(len(sorted_p)):
            position = Message.find_position(sorted_p[i], probs)
            sorted_c.append(chars[position]) 
            chars.pop(position)
            probs.pop(position)

        return sorted_c, sorted_p

    #This needs to be classmethod to be accessed from method sort, which needs to be accessed from method from another class
    #Maybe not the best way to do so (idk yet)
    @classmethod
    def find_position(cls, prob, probs):
        for position in range(len(probs)):
            if probs[position] == prob:
                return position


class Node:
    def __init__(self, char, num):
        self.char = char
        self.num = num
        self.left = None
        self.right = None
        self.code = ""
        self.seen = False

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right


class Huff:
    def __init__(self, msg):
        self.dic = {}
        self.encoded = {}
        temp = Message(msg)
        x, y = temp.get_data()
        self.chars = x[:]
        self.probs = y[:]
        self.list_c = []
        self.list_p = []

    def summarize(self):
        for i in range(len(self.chars)):
            self.list_c.append(self.chars.copy())
            self.list_p.append(self.probs.copy())
            self.sum_two()
        
        try:
            for i in range(len(self.list_c)):
                for j in range(len(self.list_c[i])):
                    if self.list_c[i][0] + self.list_c[i][1] == self.list_c[i + 1][j]:
                        # print(self.list_p[i][0], "+", self.list_p[i][1], "=", self.list_p[i + 1][j]) #This lines prints "pyramid" to see the algoritm (commented out, bcs no needed)
                        # print(self.list_c[i][0], "+", self.list_c[i][1], "=", self.list_c[i + 1][j])
                        root = self.instantiation(i ,j)
                        break
                        
        except IndexError:
            self.encode(root)
            print(self.encoded)
            return self.encoded

    def sum_two(self):
        min_c, min_p = self.get_min()
        self.remove_min()
        if (self.chars and self.probs):
            min_c2, min_p2 = self.get_min()
            self.remove_min()
            self.add_min(min_c + min_c2, min_p + min_p2)
        self.chars, self.probs = Message.sort(self, self.chars, self.probs)
        
    def get_min(self):
        min_c = self.chars[0] 
        min_p = self.probs[0]   

        return min_c, min_p     

    def remove_min(self):
        self.chars.pop(0)
        self.probs.pop(0)

    def add_min(self, min_c, min_p):
        self.chars.append(min_c)
        self.probs.append(min_p)

    def instantiation(self, i, j):
        if self.list_c[i][0] not in self.dic:
            left_node = Node(self.list_c[i][0], self.list_p[i][0])
            self.dic[self.list_c[i][0]] = left_node
        else:
            left_node = self.dic[self.list_c[i][0]]

        if self.list_c[i][1] not in self.dic:
            right_node = Node(self.list_c[i][1], self.list_p[i][1])
            self.dic[self.list_c[i][1]] = right_node
        else:
            right_node = self.dic[self.list_c[i][1]]

        if self.list_c[i + 1][j] not in self.dic:
            root = Node(self.list_c[i + 1][j], self.list_p[i + 1][j])
            self.dic[self.list_c[i + 1][j]] = root
        else: #This is probably useless
            root = self.dic[self.list_c[i + 1][j]]

        root.set_left(left_node)
        root.set_right(right_node)

        return root

    def encode(self, root, last_code = "", side = None):
        if root.left != None:
            if not root.left.seen:
                root.left.code = root.code + "0"
                root.left.seen = True
                self.encode(root.left, root.code, "left")
        else:
            if side == "left":
                root.code = last_code + "0"
                self.encoded[root.char] = root.code

                return
        
        if root.right != None:
            if not root.right.seen:
                root.right.code = root.code + "1"
                root.right.seen = True
                self.encode(root.right, root.code, "right")
        else:
            if side == "right":
                root.code = last_code + "1"
                self.encoded[root.char] = root.code

    def Kraft_inequality(self):
        count = 0
        for i in self.encoded:
            count += 2**(-len(self.encoded[i]))
        if count <= 1:
            print("Kraft inequality is correct!", "\nKraft inequality: ", count)
            return True



h = Huff("This is my awesome project!")
h.summarize()
h.Kraft_inequality()
