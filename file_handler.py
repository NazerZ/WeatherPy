
class file_handler:
    
    @staticmethod
    def opentxt():
        #grabs first line of textfile
        
        with open('key.txt', 'r') as file:
        # Read the first line
            first_line = file.readline()
        return first_line
