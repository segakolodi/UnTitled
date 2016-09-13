import urllib
import Image
import os
import math

class Gmaps:
    def __init__(self, lat, lng, zoom=16):
        """
        Args:
            lat: The latitude of the location required
            lng: The longitude of the location required
        
        """
        
        self.lat = lat
        self.lng = lng
        self.zoom = zoom
        
    def getXY(self):
        tile_size = 256
        numTiles = 1 << self.zoom
        
        # Find the x_point given the longitude
        point_x = (tile_size/2 + self.lng * tile_size / 360.0) * numTiles // tile_size
        
        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self.lat * (math.pi / 180.0))
        
        # Calcualte the y coordiante
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y)/1 - sin_y) * -(tile_size / (2 * math.pi))) * numTiles // tile_size
        
        return int(point_x), int(point_y)
        
    def generateImage(self, **kwargs):
        """
        Args:
            start_x:    The top-left x-tile coordinate
            start_y:    The top-left y-tile coordinate
            tile_width: The number of tiles wide the image should be - defaults to 5
            tile_height:The number of tiles high the image should be - defaults to 5
            
            returns:    A high-resolution google map image
        """
        
        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 5)
        tile_height = kwargs.get('tile_height', 5)
        
        # Check the tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()
            
        # Create image with size
        map_img = Image.new('RGB', (width,height))
        
        for x in range(0, tile_width):
            for y in range(0, tile_height):
                url = 'https://mt0.google.com/vt?x=' + str(start_x+x) + '&y=' + str(start_y+y) + '&z=' + str(self.zoom)
                
                current_tile = str(x) + '-' + str(y)
                urllib.urlretrieve(url, current_tile)
                
                im = Image.open(current_tile)
                map_img.paste(im, (x*256, y*256))
                os.remove(current_tile)
                
        return map_img
        

def main():
    # class instance
    gmd = Gmaps(-26.1905463, 28.0304474, 16)
    
    print("The tile coordinates are {}".format(gmd.getXY())
    
    try:
        img = gmd.generateImage()
        
    except IOError:
        print("Could not generate the image - try adjusting the zoom level and check your coordinates")
        
    else:
        img.save("Wits_East.png")
        print("The map has successfuly been created")
        
if __name__ == '__main__': main()
        
        
