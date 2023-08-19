import cssbeautifier 

class DynamicCSS:

    root = '.'

    def __init__(self, filename, default_css, replace_dict={}):
        self.filename   = filename
        self.css        = default_css
        self.replace    = replace_dict
        self.load()

    def get(self):
        # TODO: translate replace_dict vars at css
        return self.css

    def load(self):
        try:
            with open(f'{DynamicCSS.root}/css/{self.filename}.css', 'r') as input:
                self.css = input.read()
        except FileNotFoundError:
            print(f"W: CSS Override for '{self.filename}' not found; Generating file...")
            self.save()

    def save(self): 
        try:
            with open(f'{DynamicCSS.root}/css/{self.filename}.css', 'w') as input:
                input.write( cssbeautifier.beautify(self.css ))
        except Exception as E:
            print(f"E: Cannot write CSS Override for '{self.filename}' : {str(E)}")

