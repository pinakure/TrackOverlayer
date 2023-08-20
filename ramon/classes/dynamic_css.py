from classes.log        import Log

def beautify(input):
    output = input.replace('{', '{\n\t')
    output = output.replace(';', ';\n\t')    
    output = output.replace('}', '\n}\n')
    return output

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
            Log.info(f"Loaded CSS Override for '{self.filename}'.")
        except FileNotFoundError:
            Log.warning(f"CSS Override for '{self.filename}' not found; Generating file...")
            self.save()

    def save(self): 
        try:
            with open(f'{DynamicCSS.root}/css/{self.filename}.css', 'w') as input:
                input.write( beautify(self.css ))
        except Exception as E:
            Log.error(f"Cannot write CSS Override for '{self.filename}' : {str(E)}")

