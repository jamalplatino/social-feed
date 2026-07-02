class PostResponse:
    def jsonEncode(self, data): 
        return {
            "title": data['title'],
            "content": data['content']
        }
    
    