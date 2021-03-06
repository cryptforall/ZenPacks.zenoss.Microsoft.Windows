##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016-2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

'''
Utilities that may cause Zope stuff to be imported.
'''
from . import schema

from Products.ZenUtils.ZenTales import talesEvalStr


class BaseDevice(schema.BaseDevice):
    '''
    Provides common functionality for Device and ClusterDevice.
    '''

    def __init__(self, id, buildRelations=True):
        '''
        Initialize a new device.

        Overridden so that the os property can be created as subclass
        of the standard OperatingSystem class.
        '''
        super(schema.BaseDevice, self).__init__(id, buildRelations=buildRelations)
        # override OperatingSystem with our own
        try:
            self._delOb('os')
        except Exception as e:
            self.LOG.warn('Error removing OperatingSystem (%s)' % e)
        from ZenPacks.zenoss.Microsoft.Windows.OperatingSystem import OperatingSystem
        os = OperatingSystem()
        try:
            self._setObject('os', os)
        except Exception as e:
            self.LOG.info("ERROR SETTING OS: %s" % e)

    def windows_user(self):
        """Return Windows user for this device."""
        if self.getProperty('zWinRMUser'):
            return self.getProperty('zWinRMUser')

        # Fall back to old ZenPack's zWinUser or an empty string.
        return self.getProperty('zWinUser') or ''

    def windows_password(self):
        """Return Windows password for this device."""
        if self.getProperty('zWinRMPassword'):
            return self.getProperty('zWinRMPassword')

        # Fall back to old ZenPack's zWinPassword or an empty string.
        return self.getProperty('zWinPassword') or ''

    def windows_servername(self):
        """Return Windows server name for this device."""
        pname = 'zWinRMServerName'
        pvalue = self.getProperty(pname)
        if pvalue:
            try:
                return talesEvalStr(pvalue, self)
            except Exception:
                self.LOG.warn(
                    "%s.%s contains invalid TALES expression: %s",
                    self.id, pname, pvalue)

        # Fall back to an empty string.
        return ''

    def kerberos_rdns(self):
        """Return reverse dns setting.
        It should only be set at the
        /Server/Microsoft device class level.
        """
        try:
            org = self.getDmd().Devices.getOrganizer('/Server/Microsoft')
        except Exception:
            return False

        disable_rdns = org.getProperty('zWinRMKrb5DisableRDNS') or False
        return disable_rdns
