from django.db import models

import xmlrpclib
# Create your models here.
from supervisor.states import ProcessStates


class ServerGroup(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Server(models.Model):
    group = models.ForeignKey(ServerGroup)
    hostname = models.CharField(max_length=200)
    port = models.PositiveSmallIntegerField(default=9001)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    _supervisor = None
    def get_auth(self):
        if len(self.username) > 0   and   len(self.password) > 0:
            return '%s:%s@' % (self.username, self.password)

    def __unicode__(self):
        return 'http://%s@%s:%d' % (self.username, self.hostname, self.port)

    def get_supervisor(self):
        if not self._supervisor:
            c = xmlrpclib.Server('http://%s%s:%d/RPC2' % (self.get_auth(), self.hostname, self.port) )
            self._supervisor = c.supervisor
        return self._supervisor

    def get_status(self):
        try:
            return self.get_supervisor().getAllProcessInfo()
        except:
            return None

    def perform_action(self, process, action):
        print(action, process)
        supervisor = self.get_supervisor()
        status =  supervisor.getProcessInfo(process)
        if action == 'start':
            if status.get('state', None) not in (ProcessStates.RUNNING, ProcessStates.STARTING):
                supervisor.startProcess(process, True)
        elif action == 'restart':
            if status.get('state', None) in (ProcessStates.RUNNING,):
                supervisor.stopProcess(process, True)
                supervisor.startProcess(process, True)
            pass
        elif action == 'stop':
            if status.get('state', None) not in (ProcessStates.STOPPING, ProcessStates.STOPPED):
                supervisor.stopProcess(process, True)
            pass
        else:
            raise("No such action")
            pass

