import configparser
import os


class Persistence():
    """
        The Persistence class is a wrapper around the configparser module and 
        provides methods for easily handling a configuartion file for persistent
        settings.
    """
    def __init__(self) -> None:
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = os.path.join(self.CURRENT_PATH, "config")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, ".key.conf")
        self.config = configparser.ConfigParser()
        
    def openConfig(self) -> bool:
        """
            Loads the config file to allow read/write operations.   
        """
        try:
            self.config.read(f"{self.CONFIG_FILE}")
            return True
        except FileNotFoundError:
            print(f"{self.openConfig.__name__}()\nFileNotFoundError: {self.CONFIG_FILE} not found! Can't open configuration")
            return False
        except IOError:
            print(f"{self.openConfig.__name__}()\nIOError: Error while opening configuration.")
            return False
        except Exception as e:
            print(f"{self.openConfig.__name__}()\nException: Error while opening configuration.\n{repr(e)}")
            return False

    def getOption(self, _section: str, _option: str) -> (str | bool):
        """
            Get the value of a given option.        
        """
        try:
            _value = self.config.get(f"{_section}", f"{_option}")
            return _value
        except:
            print(f"{self.getOption.__name__}()\nError getting option: {_option}")
            return False
            
    def setOption(self, _section: str, _option: str, _new_value: str) -> bool:
        """
            Set the value of a given option.
        """
        try:
            self.config.set(f"{_section}", f"{_option}", f"{_new_value}")
            return True
        except:
            print(f"{self.setOption.__name__}()\nError setting option: {_option}")
            return False
            
    def addOption(self, _section: str, _new_option: str, _value: str) -> bool:
        """
            Create a new config option.
        """
        try:
            if not self.optionExists(f"{_section}", f"{_new_option}"):
                self.config.set(f"{_section}", f"{_new_option}", f"{_value}")
                return True
            return False
        except:
            print(f"{self.addOption.__name__}()\nError adding option: {_new_option}")
            return False

    def removeOption(self, _section: str, _option: str) -> bool:
        """
            Remove a configuration option.
        """
        try:
            self.config.remove_option(f"{_section}", f"{_option}")
            return True
        except:
            print(f"{self.removeOption.__name__}()\nError removing option: {_option}")
            return False
        
    def sectionExists(self, _section: str) -> bool:
        """
            Check if a configuration section exists.
        """
        try:
            if self.config.has_section(f"{_section}"):
                return True
            return False
        except:
            print(f"{self.sectionExists.__name__}()\nError checking section [{_section}] existence option")
            return False
        
    def optionExists(self, _section: str, _option: str) -> bool:
        """
            Check if a configuration option exists.
        """
        try:
            if self.config.has_section(f"{_section}"):
                if self.config.has_option(f"{_section}", f"{_option}"):
                    return True
                else:
                    return False
            else:
                return False
        except:
            print(f"{self.optionExists.__name__}()\nError checking if option: [{_option}] exists")
            return False
        
    def addSection(self, _section: str) -> bool:
        """
            Add a new configuration section.
        """
        try:
            if not self.sectionExists((f"{_section}")):
                self.config.add_section(f"{_section}")
                return True
            return False
        except:
            print(f"{self.addSection.__name__}()\nError adding section: {_section}")
            return False

    def removeSection(self, _section: str) -> bool:
        """
            Remove a configuration section.
        """
        try:
            if self.config.has_section(f"{_section}"):
                self.config.remove_section(f"{_section}")
                return True
            else:
                print(f"Section '{_section}' doesn't exist.")
                return False
        except:
            print(f"{self.removeSection.__name__}()\nError removing section: {_section}")
            return False    

    def setDefaultSection(self, _section: str) -> bool:
        """
            Set the name of the defaults section.
        """
        try:
            if len(_section) != 0:
                self.config.default_section = _section
                return True
            return False
        except:
            print(f"{self.setDefaultSection.__name__}()\nError setting default section: {_section}")
            return False
          
    def getDefaultOptionValues(self) -> (dict | bool):
        """
            Retrieve a dictionary containing the default values from the parser.
            The dictionary represents the options and their corresponding default 
            values present in the default section.   
        """
        try:
            return self.config.defaults()
        except:
            print(f"{self.getDefaultOptionValues.__name__}()\nError getting default option values.")
            return False
        
    def saveConfig(self) -> bool:
        """
            Save the configuration after operations.
        """
        try:
            with open(self.CONFIG_FILE, "w") as config_file:
                self.config.write(config_file)
                return True
        except FileNotFoundError:
            print(f"{self.saveConfig.__name__}()\nFileNotFoundError: {self.CONFIG_FILE} not found! Can't save configuration")
            return False
        except IOError:
            print(f"{self.saveConfig.__name__}()\nIOError: Error while saving configuration.")
            return False
        except Exception as e:
            print(f"{self.saveConfig.__name__}()\nException: Error while saving configuration.\n{repr(e)}")
            return False

    def updateConfig(self, _parser: configparser.ConfigParser) -> bool:
        """
            Merge another config file with this one.
        """
        try:
            self.config.update(_parser)
            return True
        except FileNotFoundError:
            print(f"{self.updateConfig.__name__}()\nFileNotFoundError: File/s not found! Can't update configuration")
            return False
        except IOError:
            print(f"{self.updateConfig.__name__}()\nIOError: Error while updating configuration.")
            return False
        except Exception as e:
            print(f"{self.updateConfig.__name__}()\nException: Error while updating configuration.\n{repr(e)}")
            return False
        
    def resetConfig(self):
        """
            Reset all configuration sections and options. This won't delete the configuration
            file itself, but rather only reset the settings. If you have defaults set they
            will go back to those.
        """
        try:
            self.config.clear()
            return True
        except:
            print(f"Error resetting configuration!")
            return False
    

