class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_node(self, node_data):
        node = SinglyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node


        self.tail = node

def compare_lists(llist1, llist2):
    while llist1.data == llist2.data:
        llist1 = llist1.next
        llist2 = llist2.next
        if llist1 is None or llist2 is None:
            return llist1 == llist2
    return 0