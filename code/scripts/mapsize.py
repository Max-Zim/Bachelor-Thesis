import rospy
from nav_msgs.msg import OccupancyGrid
from datetime import datetime

class MapSubscriber:
    def __init__(self):
        print("init")
        self.first_map_time = None
        self.map_subscriber = rospy.Subscriber("/map", OccupancyGrid, self.map_callback)

    def map_callback(self, map_data):
        if self.first_map_time is None:
            self.first_map_time = datetime.now()
        
        elapsed_time = (datetime.now() - self.first_map_time).total_seconds()
        
        # As each cell is represented by an int8_t (1 byte)
        memory_per_cell_bytes = 1
        number_of_cells = len(map_data.data)
        memory_usage_kb = (number_of_cells * memory_per_cell_bytes) / 1024
        
        print(f"{elapsed_time:.2f} | {memory_usage_kb:.2f} KB")

if __name__ == "__main__":
    rospy.init_node('map_memory_monitor', anonymous=True)
    map_subscriber = MapSubscriber()
    rospy.spin()
