import pysnmp.entity.rfc3413.oneliner.cmdgen as cmdgen
from pysnmp.smi import builder, view
from pysnmp.smi.error import SmiError


class Snmpy(object):
    '''
    Simple pysnmp wrapper.
    '''
    ERROR_MSG = 'SNMP%s of %s on %s failed.'
    PREVIOUS_EXPORT = 'already exported'
    VERSION_2_2C = 1

    def __init__(self, host, public, private, port=161, timeout=1, retries=2):
        '''
        Create the snmpy object.
        :param host: hostname or IP address of the device to communicate with
        :type host: str
        :param public: public community string
        :type public: str
        :param private: private community string
        :type private: str
        :param port: port number to connect on (default 161)
        :type port: int
        :param timeout: timeout, in seconds (default 1s)
        :type timeout: int
        :param retries: number of retries (default 2)
        :type retries: int
        :returns:
        '''
        self._host = host
        self._port = port
        self._timeout = timeout
        self._retries = retries
        self._transport = cmdgen.UdpTransportTarget((self._host, self._port),
                                                    timeout=self._timeout,
                                                    retries=self._retries)
        self._public = cmdgen.CommunityData(public, self.VERSION_2_2C)
        self._private = cmdgen.CommunityData(private, self.VERSION_2_2C)

        self._mibBuilder = builder.MibBuilder()
        self._mibViewController = view.MibViewController(self._mibBuilder)

        # Preload some commonly used modules.
        self.load_mibs('SNMPv2-MIB', 'IF-MIB', 'IP-MIB',
                       'HOST-RESOURCES-MIB', 'FIBRE-CHANNEL-FE-MIB')

    def add_mib_path(self, *path):
        '''
        Add an additional directory to the MIB search path.
        :param path: path to additional MIBs
        '''
        mibPath = self._mibBuilder.getMibPath() + path
        self._mibBuilder.setMibPath(*mibPath)

    def load_mibs(self, *modules):
        '''
        Load one or more additional MIBs.
        :param modules: modules to load
        '''
        for module in modules:
            try:
                self._mibBuilder.loadModules(module)
            except SmiError, e:
                if self.PREVIOUS_EXPORT in str(e):
                    continue
                raise

    def get(self, oid):
        '''
        Get a specific value from an OID in the SNMP tree.
        :param oid: OID to get
        :returns: value from the specified OID
        '''
        noid = self.__node_id(oid)
        (errorIndication, errorStatus, errorIndex, varBinds) = \
            cmdgen.CommandGenerator().getCmd(
                self._public,
                self._transport,
                noid)
        if errorIndication:
            raise RuntimeError(self.ERROR_MSG % ('get', oid, self._host))

        return varBinds[0][1]

    def set(self, oid, value):
        '''
        Set a specific value to an OID in the SNMP tree.
        :param oid: OID to set
        :param value: value to set
        '''
        initial_value = self.get(oid)
        set_value = type(initial_value)(str(value))
        noid = self.__node_id(oid)
        (errorIndication, errorStatus, errorIndex, varBinds) = \
            cmdgen.CommandGenerator().setCmd(
                self._private,
                self._public,
                (noid, set_value)
            )
        if errorIndication:
            raise RuntimeError(self.ERROR_MSG % ('set', oid, self._host))

        return varBinds[0][1]

    def __node_id(self, oid):
        '''
        Translate a named OID to the dotted-decimal format.
        :param oid: OID to translate
        '''
        ids = oid.split('.')
        symbols = ids[0].split('::')
        ids = tuple([int(x) for x in ids[1:]])
        mibnode, = self._mibBuilder.importSymbols(*symbols)
        oid = mibnode.getName() + ids

        return oid
