

class InventoryTracker:
    def __init__(self):
        self.blocks_at_locations = {"block1":"c1", "block2":"c2", "block3":"b1"}
        
    def remove_block(self, block):
        print("Removing " + block + " from inventory of " + str(list(self.blocks_at_locations.keys())))
        del self.blocks_at_locations[block]
        print("New blocks: " + str(list(self.blocks_at_locations.keys())) + "...")

        
        
        
