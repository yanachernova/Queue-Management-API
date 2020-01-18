from twilio.rest import Client
class AdminQueue:
    def __init__(self):
        self.account_sid = 'AC79048ee85879e1e9415f2af5111142c5'
        self.auth_token = 'a355116fd11da776ba228b585a86e4d5'
        self.client = Client(self.account_sid, self.auth_token)
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item):
        #### Aqui deben añadir a la cola ####
        self._queue.append(item)
        message = self.client.messages.create(
                              body='Beers today! '  + str(item['name']) + ' this is how much people to grab a beer before you ' + str(self.size()) + ', loozer',
                              from_='+15803804154',
                              to= str(item['phone'])
                          )
        return message.sid
        #####################################
    
    def dequeue(self):
        #### Aqui deben procesar la cola ####
        if self.size() > 0:
            if self.mode == 'FIFO':
                item = self._queue.pop()
                return item
            elif self._mode == 'LIFO':
                item = self._queue.pop(-1)
                return item
        else:
            msg = {
                "msg": "Fila sin elementos"
            }
            return msg
        #####################################

    def get_queue(self):
        ####    Retornar Toda la Fila    ####
        return self._queue
        #####################################

    def size(self):
        return len(self._queue)