# class describes method to parse a txt file with a list of urls and return a list of urls, it can also remove a url and move it to another list
# allowing to keep track of which urls have been parsed already and which didn't yet

class URLManager:
    def __init__(self, txt_filepath: str):
        self.txt_filepath = txt_filepath # stores the input file source
        self.urls = [] # initializes an empty list (of strings)
        self.parsed_urls = [] # initializes an empty list for the urls that have been succesfully parsed 
        self._load_urls() # processes the input
        

    def _load_urls(self):
        if self.txt_filepath.startswith("http"): # if by any chance, instead of a txt file, a url is given directly
            self.urls = self.txt_filepath # returns a list with a single url
        # if it is a txt file with url
        elif self.txt_filepath.endswith(".txt"): # checks that the file is a txt file
            # Read the file and return the URLs. I chose this method because my files are small and I can read them all at once.
            # If the file is large, I would use a generator to read line by line. "for line in open(input): yield line.strip()" 
            with open(self.txt_filepath, "r") as url_list:
                url_to_parse = url_list.readlines()  # reading lines of the txt file
                url_to_parse = [url.strip() for url in url_to_parse if url.strip()]  # cleaning /n and empty lines
                self.urls = url_to_parse
        else:
            raise ValueError("Input must be a URL or a .txt file with URLs")

    def get_urls(self) -> list:
        return self.urls # returns the urls list
    
    def get_url_count(self) -> int:
        return len(self.urls) # returns len of url list
    
    def remove_url(self): # function to remove the first url of the list and add it to another list
        self.parsed_urls.append(self.urls[0])
        self.urls = self.urls[1:]
        
    
# example use

# url_loader = URLManager("RAW_DATA/PARSED_ACL_URL.txt")
# url_list = url_loader.get_urls()

# print(url_list) # prints the list of urls 
# print(url_loader.parsed_urls) # prints the list of parsed urls
# print(url_loader.txt_filepath, url_loader.get_url_count()) # prints the input filepath and the number of urls in the list
# print(url_loader.remove_url()) # removes the first url of the list
# print(url_loader.parsed_urls)  # prints the list of parsed urls