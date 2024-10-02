import logging
import os
from datetime import datetime

file_name=f"{datetime.now().strftime('%m %d %Y %H %M %S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",file_name)
os.makedirs(logs_path,exist_ok=True)

logging.basicConfig(
    filename=os.path.join(logs_path,file_name),
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)


