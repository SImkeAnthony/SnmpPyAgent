class USer:

    def __init__(self, name, authProtocol, authName, chifProtocol, chifName, securityLevel):
        self.name = name
        self.authProtocol = authProtocol
        self.authName = authName
        self.chifProtocol = chifProtocol
        self.chifName = chifName
        self.securityLevel = securityLevel

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getAuthProtocol(self):
        return self.authProtocol

    def setAuthProtocol(self, authProtocol):
        self.authProtocol = authProtocol

    def getAuthName(self):
        return self.authName

    def setAuthName(self, authName):
        self.authName = authName

    def getChifProtocol(self):
        return self.chifProtocol

    def setChifProtocol(self, chifProtocol):
        self.chifProtocol = chifProtocol

    def getChifName(self):
        return self.chifName

    def setChifName(self, chifName):
        self.chifName = chifName

    def getSecurityLevel(self):
        return self.securityLevel

    def setSecurityLevel(self, securityLevel):
        self.securityLevel = securityLevel

