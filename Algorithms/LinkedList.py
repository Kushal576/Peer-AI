class node:
    def __init__(self,data):
        self.data=data
        self.next=None

class linkedlist:
    def __init__(self):
        self.head=None

    def insert(self,data):
        new_node=node(data)
        if(self.head==None):
            self.head=new_node
            return
        nextptr=self.head
        if(nextptr.data>data):
            new_node.next=self.head
            self.head=new_node
        while(nextptr.next!=None and nextptr.next.data<data):
            nextptr=nextptr.next
        new_node.next=nextptr.next
        nextptr.next=new_node

    def traverse(self):
        ptr=self.head
        while(ptr):
            print(ptr.data)
            ptr=ptr.next


