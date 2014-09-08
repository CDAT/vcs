'''
Created on Jun 18, 2014

@author: tpmaxwel
'''

import Canvas
import VCS_validation_functions
import AutoAPI
import xmldocs
import cdtime, multiprocessing
import vcs
import DV3D
from DV3D.ConfigurationFunctions import ConfigManager

class Gfdv3d(object,AutoAPI.AutoAPI):

    __slots__ = [
         '__doc__',
         'name',
         'axes'
         ]
    
    def _getname(self):
        return self._name    
    def _setname(self,value):
        value=VCS_validation_functions.checkname(self,'name',value)
        if value is not None:
            self._name=value            
    name=property(_getname,_setname)
    
    def _getaxes(self):
        return self._axes
    def _setaxes(self,value):
        value=VCS_validation_functions.checkOnOff(self,'axes',value)
        self._axes=value
    axes=property(_getaxes,_setaxes)

    def _getNumCores(self):
        return self.ncores
    def _setNumCores(self, nc ):
        self.ncores = nc
    NumCores=property(_getNumCores,_setNumCores)
    
    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):
        if not isinstance(Gfdv3d_name,str):
            raise ValueError,"DV3D name must be a string"
        if Gfdv3d_name in vcs.elements[self.g_name].keys():
            raise ValueError,"DV3D graphic method '%s' already exists" % Gfdv3d_name
        self._name = Gfdv3d_name
        self._plot_attributes = {}
        self.projection = 'default' 
        self.provenanceHandler = None
                
        if Gfdv3d_name=="xyt": 
            self._axes="xyt"
        else:
            self._axes="xyz"

        self.cfgManager = ConfigManager()  
        self.ncores = multiprocessing.cpu_count()           
        self.addParameters()
            
        vcs.elements[self.g_name][Gfdv3d_name]=self
        print "Adding VCS element: %s %s " % ( self.g_name, Gfdv3d_name )
        
    def setProvenanceHandler(self, provenanceHandler ):
        self.provenanceHandler = provenanceHandler
                
    def getStateData(self):
        return self.cfgManager.getStateData()

    def getConfigurationData( self, **args ):
        return self.cfgManager.getConfigurationData( **args )
    
    def getConfigurationState( self, pname ):
        return self.cfgManager.getConfigurationState( pname )

    def add_property(self, name ):
        fget = lambda self: self.getParameter(name)
        fset = lambda self, value: self.setParameter(name, value)
        setattr(self.__class__, name, property(fget, fset))

    def addPlotAttribute(self, name, value ):
        self._plot_attributes[ name ] = value 

    def getPlotAttribute(self, name ):
        return self._plot_attributes.get( name, None )

    def getPlotAttributes( self ):
        return self._plot_attributes
    
    @staticmethod
    def getParameterList():
        cfgManager = ConfigManager()
        parameterList = cfgManager.getParameterList()
        return parameterList
                
    def addParameters( self ):
        self.parameter_names = []
        for pname in self.getParameterList():
            self.add_property( pname )
            self.parameter_names.append( pname )
#            print "  ------------->> Adding parameter: ", pname
            
    def getParameter(self, param_name, **args ):
        return self.cfgManager.getParameterValue( param_name, **args )

    def setParameter(self, param_name, data, **args ):
        self.cfgManager.setParameter( param_name, data, **args )
        
    def restoreState(self):
        self.cfgManager.restoreState()

    def initDefaultState(self):
        self.cfgManager.initDefaultState()
                
    def list(self):
        print ' ---------- DV3D (Gfdv3d) member (attribute) listings ---------'
        print 'name =',self.name
        print 'axes =',self.axes
        for pname in self.parameter_names:
            print ' = '.join( [ pname, self.getParameter( pname ) ] )

class Gf3Dvector(Gfdv3d):

    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):        
        self.g_name='3d_vector'                        
        Gfdv3d.__init__(self, Gfdv3d_name, Gfdv3d_name_src='default')

class Gf3Dscalar(Gfdv3d):

    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):        
        self.g_name='3d_scalar'                        
        Gfdv3d.__init__(self, Gfdv3d_name, Gfdv3d_name_src='default')
        self.VectorDisplay = Gfdv3d_name

