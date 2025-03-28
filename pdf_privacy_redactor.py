import os
import fitz  # PyMuPDF

class PDF_Privacy_Redactor:
    def __init__(self):
        self.filepath = None
        self.file = None
        self.tokens = {}

    def loadDocument(self, input_file: str) -> None:
        if os.path.exists(input_file):
            self.filepath = input_file
            self.file = fitz.open(self.filepath)
        else:
            raise Exception("File does not exists")

    def saveDocument(self, output_file: str):
        self.file.save(output_file)
        self.file.close()

    def listPattern(self) -> dict:
        return self.tokens
    
    def getPattern(self, key: str) -> str:
        if key not in self.tokens:
            return None
        return self.tokens[key]
    
    def addPattern(self, token: str) -> None:
        if token in self.tokens.values():
            raise Exception("Pattern already exists")
        self.tokens[len(self.tokens.keys())] = token

    def removePattern(self, key: str) -> None:
        if key not in self.tokens.keys():
            raise Exception("No such key found")
        self.tokens.pop(key)

    def identify(self) -> list:
        matches = {}
        for page_num in range(len(self.file)):
            page = self.file.load_page(page_num)
            
            for index, token in self.tokens.items():
                text = page.search_for(token)
                if len(text):
                    if page_num not in matches:
                        matches[page_num] = []
                    matches[page_num].append((index, text))
        return matches

    def redact_page(self, page_num: int) -> None:
        count = 0
        page = self.file[page_num]
        for _, token in self.tokens.items():
            text_instances = page.search_for(token)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))
                count += 1
        page.apply_redactions()
        print("[!] Tokens Redacted:", count)

    def redact(self) -> None:
        count = 0
        # Loop over all the pages and redact
        for page in self.file:
            for index, token in self.tokens.items():
                text_instances = page.search_for(token)
                for inst in text_instances:
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                    count += 1
            page.apply_redactions()
        print("[!] Tokens Redacted:", count)
        

