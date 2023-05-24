from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import context, cmdrsp
from user.User import USer
from pysnmp.proto.api import v2c
from pysnmp.smi import instrum, builder

class SnmpAgent:
    def __init__(self, ipAddress, port):
        self.engine = engine.SnmpEngine()
        self.ipAddress = ipAddress
        self.port = port
        self.userList = []
        self.snmpContext = None

    def initTransport(self):
        print("Initialize transport ...")
        config.addTransport(
            self.engine,
            udp.domainName,
            udp.UdpTransport().openServerMode((self.ipAddress, self.port))
        )

    # initialize context of snmp engine
    def initContext(self):
        print("Set context ...")
        self.snmpContext = context.SnmpContext(
            self.engine,
            contextEngineId=v2c.OctetString(hexValue='8000000001020304')
        )
        self.snmpContext.registerContextName(
            v2c.OctetString("contextPrivate"),
            instrum.MibInstrumController(builder.MibBuilder())
        )

    # init the dispatcher for a never ending job
    def initRunningDispatcher(self):
        print("Initialize dispatcher running job ...")
        self.engine.transportDispatcher.jobStarted(1)
    """
    Configuration for SNMPv3
    """

    # Here add user to configuration
    def initUSMUserV3(self):
        print("Initialize users ...")
        user = USer("anthony", config.usmHMACMD5AuthProtocol, "Silver-Major-Knight-16", config.usmDESPrivProtocol,
                    "Silver-Major-Knight-17", "authPriv")
        self.userList.append(user)
        for user in self.userList:
            config.addV3User(
                self.engine,
                user.getName(),
                user.getAuthProtocol(),
                user.getAuthName(),
                user.getChifProtocol(),
                user.getChifName()
            )

    # Here add Vacm to allow access view for users
    def initVacmMIBV3(self):
        print("Initialize VacmMIB ...")
        # Allow full access for each user
        for user in self.userList:
            config.addVacmUser(
                self.engine,
                3,
                user.getName(),
                user.getSecurityLevel(),
                (1, 3, 6, 1, 2, 1),
                (1, 3, 6, 1, 2, 1)
            )

    # register snmp application to the snmp engine
    def registerSnmpAppV3(self):
        print("Register Snmp application ...")
        cmdrsp.GetCommandResponder(self.engine, self.snmpContext)

    # all init
    def initSnmpV3(self):
        self.initTransport()
        self.initUSMUserV3()
        self.initVacmMIBV3()
        self.initContext()
        self.registerSnmpAppV3()
        self.initRunningDispatcher()

    """
    Configuration for SNMPv1
    """
    def initSecurityNameV1(self):
        config.addV1System(self.engine, "Silver-King-Rogue-16", "Silver-King-Rogue-16")

    def initVacmMIBV1(self):
        config.addVacmUser(
            self.engine,
            1,
            "Silver-King-Rogue-16",
            "noAuthNoPriv",
            (1, 3, 6, 1, 2, 1)
        )

    def registerSnmpAppV1(self):
        print("Register Snmp application ...")
        cmdrsp.GetCommandResponder(self.engine, self.snmpContext)


    def initSnmpV1(self):
        self.initTransport()
        self.initVacmMIBV1()
        self.initContext()
        self.registerSnmpAppV1()
        self.initRunningDispatcher()

    """
    External methode
    """

    # Need external add user
    def addUser(self, user):
        self.userList.append(user)

    """
    Handle methode
    """
    def handle_get(slef,snmp_engine, community_data, pdu, cb_ctx):
        # Handle SNMP GET request
        # Access and process the requested OIDs from the PDU
        # Construct the response PDU with the requested values
        # Example response
        response_pdu = pdu
        print(response_pdu, " ", community_data)

    """
    Run methode
    """
    def run(self, version):
        if version == 1:
            try:
                self.initSnmpV1()
                print("Snmp agent running ...")
                self.engine.transportDispatcher.runDispatcher()
            except ConnectionError:
                print("Error occurred")
                print(ConnectionError.strerror)
            finally:
                self.engine.transportDispatcher.closeDispatcher()
                print("Snmp agent stopping")
        elif version == 3:
            try:
                self.initSnmpV3()
                print("Snmp agent running ...")
                self.engine.transportDispatcher.runDispatcher()
            except TypeError:
                print("Error occurred")
                print(ConnectionError.strerror)
            finally:
                self.engine.transportDispatcher.closeDispatcher()
                print("Snmp agent stopping")