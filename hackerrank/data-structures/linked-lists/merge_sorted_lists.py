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

def mergeLists(head1, head2):
    if head1 is None:
        return head2
    if head2 is None:
        return head1
        
    if head1.data <= head2.data:
        new_head = SinglyLinkedListNode(head1.data)
        head1 = head1.next
    else:
        new_head = SinglyLinkedListNode(head2.data)
        head2 = head2.next
        
    node = new_head
    while head1 is not None and head2 is not None:
        if head1.data <= head2.data:
            new_node = SinglyLinkedListNode(head1.data)
            head1 = head1.next
        else:
            new_node = SinglyLinkedListNode(head2.data)
            head2 = head2.next
        node.next = new_node
        node = node.next
        
    if head1 is None:
        node.next = head2
    else:
        node.next = head1
    
    return new_head