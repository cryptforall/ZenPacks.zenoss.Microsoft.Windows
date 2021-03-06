##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016-2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
from . import schema
from utils import get_rrd_path


class OSProcess(schema.OSProcess):
    '''
    Model class for OSProcess.

    Extended here to support alternate monitoring template binding.
    Depending on the version of Windows there are different per-process
    counters available.
    '''

    # preserve the old style path
    rrdPath = get_rrd_path

    def getRRDTemplateName(self):
        '''
        Return monitoring template name appropriate for this component.

        Overridden to support different per-process monitoring
        requirements for Windows 2003 servers.
        '''
        default = super(OSProcess, self).getRRDTemplateName()

        if self.supports_WorkingSetPrivate is False:
            return '-'.join((default, '2003'))

        return default
