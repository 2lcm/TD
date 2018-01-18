class NODE(object):
    def __init__(self, temp_object):
        self.head = None
        self.tail = None
        self.value = temp_object

class LL(object):
    def __init__(self):
        self.head_node = NODE(None)
        self.tail_node = NODE(None)
        self.head_node.tail = self.tail_node
        self.tail_node.head = self.head_node

    def insert(self, new_node):
        end_node = self.tail_node.head # end_node means the node that is right front of tail_node
        end_node.tail = new_node
        new_node.head = end_node
        new_node.tail = self.tail_node
        self.tail_node.head = new_node

    def delete(self, del_node):
        current_node = self.head_node.tail
        while True:
            if current_node == self.tail_node:
                print('Incomplete Delete')
                break
            if current_node == del_node:
                front_node = current_node.head
                back_node = current_node.tail
                front_node.tail = back_node
                back_node.head = front_node
                del(current_node)
                print('Perfect Delete')
                break
            current_node = current_node.tail
    def test(self):
        current_node = self.head_node
        while True:
            if current_node == self.tail_node:
                print('its done')
                break
            else:
                print(current_node.value)
                current_node = current_node.tail
A = NODE('changyeop')
B = NODE('chulmin')
C = NODE('horse')
Link = LL()
Link.insert(A)
Link.insert(B)
Link.insert(C)
Link.delete(B)
# Link.delete(A)
Link.test()
