from nodejs import node,npm,npx

class APIClient:
    def __init__(self):
        npm.call(['install', '--save', '@retroachievements/api'])

    def authorize(self):
        node.call(['js/authorize.js'])
