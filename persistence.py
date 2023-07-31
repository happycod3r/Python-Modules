import configparser
import os


class Persistence():
    """
        The Persistence class is a wrapper around the configparser module and 
        provides methods for easily handling a configuartion file for persistent
        settings. 
    """
    def __init__(self, _config_dir_name: str = None, _config_file_path: str = None) -> None:
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = os.path.join(self.CURRENT_PATH, f"{_config_dir_name}")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, f"{_config_file_path}")
        self.config = configparser.ConfigParser()
        
    #//////////// CONFIG DIRECTORY METHODS ////////////
    
    def create_config_dir(self) -> bool:
        """
        Creates the config directory passed as the first argument of the constructor.
        Returns True if successful otherwise False. Also returns False if it already 
        exists.
        """
        if not os.path.exists(self.CONFIG_DIR):
            try:
                os.mkdir(self.CONFIG_DIR)
                return True
            except FileNotFoundError:
                print("FileNotFoundError: File not found error")
                return False
            except IOError:
                print("IOError: Could not create directory.")
            except Exception as e:
                print(repr(e))
                return False
        return False    
        
    def delete_config_dir(self) -> bool:
        """
        Deletes the configuration directory passed as the first argument to the 
        constructor. Returns True if successful otherwise False. Also returns
        False if the configuration directory isn't there.
        """
        if os.path.exists(self.CONFIG_DIR):
            try:
                os.rmdir(self.CONFIG_DIR)
                return True
            except FileNotFoundError:
                print(f"{self.delete_config_dir.__name__}: Config dir not found")
                return False
            except IOError:
                print(f"{self.delete_config_dir.__name__}: IOError")
                return False
            except Exception as e:
                print(f"{self.delete_config_dir.__name__}\n{repr(e)}")
                return False 
        return False
        
    def get_config_dir_path(self) -> (str | bool):
        """
        Returns the absolute path to the config directory. Returns True if successful
        and returns False if the config doesn't exist.
        """
        if os.path.exists(self.CONFIG_DIR):
            return self.CONFIG_DIR
        return False
        
    #//////////// CONFIG FILE METHODS ////////////
        
    def create_config_file(self) -> bool:
        """
        Creates the config file passed as the second argument of the constructor
        at the path specfied in the first argument of the constructor.
        """
        if not os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'w') as file:
                    file.close()
                    return True
            except FileNotFoundError:
                print(f"File '{self.CONFIG_FILE}' already exists!")
                return False
            except IOError:
                return False
            except Exception as e:
                print(repr(e))
                return False    
    
    def delete_config_file(self):
        """
        Deletes the config file specified as the second argument to the
        constructor. Return True if successful and False otherwise.
        """
        if os.path.exists(self.CONFIG_FILE):
            try:
                os.remove(self.CONFIG_FILE)
                return True
            except FileNotFoundError:
                print(f"File '{self.CONFIG_FILE}' not found.")
                return False
            except Exception as e:
                print(f"An error occurred while trying to delete the file: {repr(e)}")
        return False
        
    def open_config(self) -> bool:
        """
            Loads the config file to allow read/write operations.   
        """
        try:
            self.config.read(f"{self.CONFIG_FILE}")
            return True
        except FileNotFoundError:
            print(f"{self.open_config.__name__}()\nFileNotFoundError: {self.CONFIG_FILE} not found! Can't open configuration")
            return False
        except IOError:
            print(f"{self.open_config.__name__}()\nIOError: Error while opening configuration.")
            return False
        except Exception as e:
            print(f"{self.open_config.__name__}()\n{repr(e)}")
            return False

    def save_config(self) -> bool:
        """
            Save the configuration after operations.
        """
        try:
            with open(self.CONFIG_FILE, "w") as config_file:
                self.config.write(config_file)
                return True
        except FileNotFoundError:
            print(f"{self.save_config.__name__}()\nFileNotFoundError: {self.CONFIG_FILE} not found! Can't save configuration")
            return False
        except IOError:
            print(f"{self.save_config.__name__}()\nIOError: Error while saving configuration.")
            return False
        except Exception as e:
            print(f"{self.save_config.__name__}()\n{repr(e)}")
            return False

    def update_config(self, _parser: configparser.ConfigParser) -> bool:
        """
            Merge another config file with this one.
        """
        try:
            self.config.update(_parser)
            return True
        except FileNotFoundError:
            print(f"{self.update_config.__name__}()\nFileNotFoundError: File/s not found! Can't update configuration")
            return False
        except IOError:
            print(f"{self.update_config.__name__}()\nIOError: Error while updating configuration.")
            return False
        except Exception as e:
            print(f"{self.update_config.__name__}()\n{repr(e)}")
            return False
        
    def reset_config(self):
        """
            Reset all configuration sections and options. This won't delete the configuration
            file itself, but rather only reset the settings. If you have defaults set they
            will go back to those.
        """
        try:
            self.config.clear()
            return True
        except Exception as e:
            print(f"{self.reset_config.__name__}\n{repr(e)}")
            return False

    def read_config(self) -> (str | bool):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as file:
                    contents = file.read()
                    if len(contents) != 0:
                        return contents
                    else: 
                        print(f"File: '{self.CONFIG_FILE}' is exists but is empty")
            except FileNotFoundError:
                print(f"File '{self.CONFIG_FILE}' not found.")
                return False
            except IOError:
                print(f"Error reading file '{self.CONFIG_FILE}'.")
                return False
            except Exception as e:
                print(repr(e))
                return False
        return False
    
    def dump_config_to_output(self) -> bool:
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as file:
                    contents = file.read()
                    if len(contents) != 0:
                        print(contents)
                        return True
                    else: 
                        print(f"File: '{self.CONFIG_FILE}' is exists but is empty")
                        return False
            except FileNotFoundError:
                print(f"File '{self.CONFIG_FILE}' not found.")
                return False
            except IOError:
                print(f"Error reading file '{self.CONFIG_FILE}'.")
                return False
            except Exception as e:
                print(repr(e))
                return False
        return False
    
    #//////////// OPTION METHODS ////////////
    
    def get_option(self, _section: str, _option: str) -> (str | bool):
        """
            Get the value of a given option.        
        """
        try:
            _value = self.config.get(f"{_section}", f"{_option}")
            return _value
        except Exception as e:
            print(f"{self.get_option.__name__}()\n{repr(e)}")
            return False
    
    def get_options(self, _section: str) -> (list | bool):
        """
        Returns a list of all options.
        """
        try:
            return self.config.options(f"{_section}")
        except Exception as e:
            print(f"{self.get_sections.__name__}()\n{repr(e)}")
            return False
            
    def set_option(self, _section: str, _option: str, _new_value: str) -> bool:
        """
            Set the value of a given option.
        """
        try:
            self.config.set(f"{_section}", f"{_option}", f"{_new_value}")
            return True
        except Exception as e:
            print(f"{self.set_option.__name__}()\n{repr(e)}")
            return False
            
    def add_option(self, _section: str, _new_option: str, _value: str) -> bool:
        """
            Create a new config option.
        """
        try:
            if not self.option_exists(f"{_section}", f"{_new_option}"):
                self.config.set(f"{_section}", f"{_new_option}", f"{_value}")
                return True
            return False
        except Exception as e:
            print(f"{self.add_option.__name__}()\n{repr(e)}")
            return False

    def remove_option(self, _section: str, _option: str) -> bool:
        """
            Remove a configuration option.
        """
        try:
            self.config.remove_option(f"{_section}", f"{_option}")
            return True
        except Exception as e:
            print(f"{self.remove_option.__name__}()\n{repr(e)}")
            return False
        
    def option_exists(self, _section: str, _option: str) -> bool:
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
        except Exception as e:
            print(f"{self.option_exists.__name__}()\n{repr(e)}")
            return False
        
    #//////////// SECTION METHODS ////////////
    
    def section_exists(self, _section: str) -> bool:
        """
            Check if a configuration section exists.
        """
        try:
            if self.config.has_section(f"{_section}"):
                return True
            return False
        except Exception as e:
            print(f"{self.section_exists.__name__}()\n{repr(e)}")
            return False
          
    def add_section(self, _section: str) -> bool:   
        """
            Add a new configuration section.
        """
        try:
            if not self.section_exists((f"{_section}")):
                self.config.add_section(f"{_section}")
                return True
            return False
        except Exception as e:
            print(f"{self.add_section.__name__}()\n{repr(e)}")
            return False

    def remove_section(self, _section: str) -> bool:
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
        except Exception as e:
            print(f"{self.remove_section.__name__}()\n{repr(e)}")
            return False    

    def get_sections(self) -> (list | bool):
        """
        Returns a list of all sections.
        """
        try:
            return self.config.sections()
        except Exception as e:
            print(f"{self.get_sections.__name__}()\n{repr(e)}")
            return False
        
    #//////////// DEFAULT SECTION/OPTION METHODS ////////////
    
    def set_default_section(self, _section: str) -> bool:
        """
            Set the name of the defaults section.
        """
        try:
            if len(_section) != 0:
                self.config.default_section = _section
                return True
            return False
        except Exception as e:
            print(f"{self.set_default_section.__name__}()\n{repr(e)}")
            return False
          
    def get_default_option_values(self) -> (dict | bool):
        """
            Retrieve a dictionary containing the default values from the parser.
            The dictionary represents the options and their corresponding default 
            values present in the default section.   
        """
        try:
            return self.config.defaults()
        except Exception as e:
            print(f"{self.get_default_option_values.__name__}()\n{repr(e)}")
            return False
        