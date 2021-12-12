import os
import logging
from logging import handlers


log_c = "./logs/"

if not os.path.exists(log_c):
    os.makedirs(log_c, exist_ok=True)

logging.basicConfig(handlers=[
                        handlers.RotatingFileHandler(filename=log_c+"sayu.log",
                                                     maxBytes=3145728,
                                                     backupCount=1),
                        logging.StreamHandler()
                              ])

sayulogs = logging.getLogger("SayuRawr")




