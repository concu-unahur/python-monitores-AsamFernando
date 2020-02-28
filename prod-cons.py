import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def productor(monitor):
    print("Voy a producir")
    for i in range(20):
        with monitor:          # hace el acquire y al final un release
            items.append(i)    # agrega un ítem
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2)


class Consumidor(threading.Thread):
    def __init__(self, monitor, cantConsumir, nroCons):
        super().__init__()
        self.monitor = monitor
        self.cantConsumir=cantConsumir
        self.nroCons=nroCons

    def run(self):
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while len(items)<self.cantConsumir:     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
                for i in range(self.cantConsumir):
                    x = items.pop(0)     # saca (consume) el primer ítem
            
            logging.info(f'consumidor {self.nroCons} Consumio {x}')
            time.sleep(1)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# un thread que consume

cons1 = Consumidor(items_monit, 3, 1)
cons2 = Consumidor(items_monit, 2, 2)
cons3 = Consumidor(items_monit, 1, 3)



cons1.start()
cons2.start()
cons3.start()

# El productor
productor(items_monit)

        
