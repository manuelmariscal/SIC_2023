    
from gpiozero import MCP3000, DistanceSensor
from time import sleep
from datetime import datetime

pot = MCP3000(7)
ultrasonic = DistanceSensor(echo = 21, trigger = 20)
file = open('./txtFiles/distance_log.txt', 'w')

def main():
    while True:
        dist = ultrasonic.distance * 100
        span = pot.value * 100 # For scaling
        dist, span = round(dist, 3), round(span, 3)
        
        if dist <= span:
            print(f"scaled span: {span}, dist: {dist}")
            timestamp = datetime.now().strftime('%Y/&m/%d - %HH %MM %SS')
            data = f"{timestamp} --> " \
                    f"distance : {dist}, span: {span}\n"
            file.write(data)
        else:
            print(f"Distance > span!! scaled span: {span}, dist: {dist}")
        sleep(1)
        
    
if __name__ == "__main__":
    main()
    file.close()
