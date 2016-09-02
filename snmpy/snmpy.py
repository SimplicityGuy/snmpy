"""Simple SNMP wrapper."""

import pysnmp.entity.rfc3413.oneliner.cmdgen as cmdgen
from pysnmp.proto import rfc1902
from pysnmp.smi import builder, view
from pysnmp.smi.error import SmiError


class Snmpy(object):
    """Simple pysnmp wrapper."""

    ERROR_MSG = 'SNMP%s of %s on %s failed.'
    PREVIOUS_EXPORT = 'already exported'
    VERSION_2_2C = 1

    # pylint: disable=too-many-arguments
    # In order to allow flexibility in this wrapper, the additional optional
    # arguments are needed.
    def __init__(self, host, public, private, port=161, timeout=1, retries=2):
        """Create the snmpy object.

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
        :returns: new Snmpy object
        :rtype: Snmpy
        """
        self._host = host
        self._port = port
        self._timeout = timeout
        self._retries = retries
        self._transport = cmdgen.UdpTransportTarget(
            (self._host, self._port),
            timeout=self._timeout,
            retries=self._retries
        )
        self._public = cmdgen.CommunityData(
            public, mpModel=self.VERSION_2_2C
        )
        self._private = cmdgen.CommunityData(
            private, mpModel=self.VERSION_2_2C
        )

        self._mib_builder = builder.MibBuilder()
        self._mib_view_controller = view.MibViewController(self._mib_builder)

        # Pre-load some commonly used modules.
        self.load_mibs('SNMPv2-MIB', 'IF-MIB', 'IP-MIB',
                       'HOST-RESOURCES-MIB', 'FIBRE-CHANNEL-FE-MIB')

    def add_mib_path(self, *path):
        """Add an additional directory to the MIB search path.

        :param path: path to additional MIBs
        """
        mib_path = self._mib_builder.getMibPath() + path
        self._mib_builder.setMibPath(*mib_path)

    def load_mibs(self, *modules):
        """Load one or more additional MIBs.

        :param modules: modules to load
        """
        for module in modules:
            try:
                self._mib_builder.loadModules(module)
            except SmiError as error:
                if self.PREVIOUS_EXPORT in str(error):
                    continue
                raise

    def get(self, oid):
        """Get a specific value from an OID in the SNMP tree.

        :param oid: OID to get
        :returns: value from the specified OID
        """
        noid = self.__node_id(oid)
        (error_indication, _, _, var_binds) = cmdgen.CommandGenerator().getCmd(
            self._public,
            self._transport,
            noid
        )
        if error_indication:
            raise RuntimeError(self.ERROR_MSG % ('get', oid, self._host))

        return var_binds[0][1]

    def set(self, oid, value):
        """Set a specific value to an OID in the SNMP tree.

        :param oid: OID to set
        :param value: value to set
        """
        initial_value = self.get(oid)
        noid = self.__node_id(oid)
        (error_indication, _, _, var_binds) = cmdgen.CommandGenerator().setCmd(
            self._private,
            self._transport,
            (noid, self.__coerce_value(initial_value, value))
        )
        if error_indication:
            raise RuntimeError(self.ERROR_MSG % ('set', oid, self._host))

        return var_binds[0][1]

    def __node_id(self, oid):
        """Translate a named OID to the dotted-decimal format.

        :param oid: OID to translate
        """
        ids = oid.split('.')
        symbols = ids[0].split('::')
        ids = tuple([int(x) for x in ids[1:]])
        mibnode, = self._mib_builder.importSymbols(*symbols)
        oid = mibnode.getName() + ids

        return oid

    @staticmethod
    def __coerce_value(initial_value, new_value):
        """Coerce the new_value to the same type as the initial_value.

        :param initial_value: initial value from the device
        :param new_value: new value to set, coerced into the right type
        :return: new value, coerced into the right type
        """
        # pylint: disable=redefined-variable-type
        # In order to return the right type the return value has to be
        # redefined.

        # Types from RFC-1902
        if isinstance(initial_value, rfc1902.Counter32):
            set_value = rfc1902.Counter32(str(new_value))
        elif isinstance(initial_value, rfc1902.Counter64):
            set_value = rfc1902.Counter64(str(new_value))
        elif isinstance(initial_value, rfc1902.Gauge32):
            set_value = rfc1902.Gauge32(str(new_value))
        elif isinstance(initial_value, rfc1902.Integer):
            set_value = rfc1902.Integer(str(new_value))
        elif isinstance(initial_value, rfc1902.Integer32):
            set_value = rfc1902.Integer32(str(new_value))
        elif isinstance(initial_value, rfc1902.IpAddress):
            set_value = rfc1902.IpAddress(str(new_value))
        elif isinstance(initial_value, rfc1902.OctetString):
            set_value = rfc1902.OctetString(str(new_value))
        elif isinstance(initial_value, rfc1902.TimeTicks):
            set_value = rfc1902.TimeTicks(str(new_value))
        elif isinstance(initial_value, rfc1902.Unsigned32):
            set_value = rfc1902.Unsigned32(str(new_value))
        else:
            raise RuntimeError("Unknown type %s" % type(initial_value))

        return set_value
