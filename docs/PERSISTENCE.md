# persistence.py

## [Table Of Contents](#toc)

- [Table of Contents](#toc)
- [About](#about)
- [Documentation](#documentation)
  - [Persistence Class](#persistence-class)
  - [Class Variables](#class-variables)
  - [Class Methods](#class-methods)

## [About](#about)

The persistence module is a wrapper class for the `configparser` module
which provides methods for easily setting up and managing a configuration
file for persistent settings. The `Persistence` class methods encapsulate
the basic functionality of `configparser` with some added methods, So it's
even easier to use than the already easy to use `configparser` module.

## [Documentation](#documentation)

### [Persistence Class](#persistence-class)

```python
class Persistence()
    def __init__(self, _config_dir: str, _config_file_abs_path: str):
```

### [Class Variables](#variables)
```python
CURRENT_PATH # Holds the current path of the persistence module.
CONFIG_DIR # Hold the path to the configuration directory.
CONFIG_FILE # Holds the path to the configuration file.
```

### [Class Methods](#class-methods)

#### create_config_dir

Creates the config directory passed as the first argument of the constructor.
Returns True if successful otherwise False. Also returns False if it already 
exists.

```python
def create_config_dir(self) -> bool:
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
```

#### delete_config_dir

Deletes the configuration directory passed as the first argument to the constructor. 
Returns True if successful otherwise False. Also returns False if the configuration 
directory isn't there.


```python
def delete_config_dir(self) -> bool:
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
        
```

#### get_config_dir_path

Returns the absolute path to the config directory. Returns True if successful 
and returns False if the config doesn't exist.

```python
def get_config_dir_path(self) -> (str | bool):
    if os.path.exists(self.CONFIG_DIR):
        return self.CONFIG_DIR
    return False
       
```

#### create_config_file

Creates the config file passed as the second argument of the constructor
at the path specfied in the first argument of the constructor.

```python
def create_config_file(self) -> bool:
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
    
```

#### delete_config_file

Deletes the config file specified as the second argument to the 
constructor. Return True if successful and False otherwise.

```python
def delete_config_file(self):
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
      
```

#### open_config

Loads the config file to allow read/write operations.

```python
def open_config(self) -> bool:
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

```

#### save_config

Save the configuration after operations.

```python
def save_config(self) -> bool:
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
```

#### update_config

Merge another config file with this one.

```python
def update_config(self, _parser: configparser.ConfigParser) -> bool:
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
```

#### reset_config

Reset all configuration sections and options. This won't delete the configuration
file itself, but rather only reset the settings. If you have defaults set they
will go back to those.

```python
def reset_config(self):
    try:
        self.config.clear()
        return True
    except Exception as e:
        print(f"{self.reset_config.__name__}\n{repr(e)}")
        return False

```

#### read_config

Returns the entire contents of the configuration file.

```python
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
    
```

#### dump_config_to_output

```python
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
    
```

#### get_option

Get the value of a given option.

```python
def get_option(self, _section: str, _option: str) -> (str | bool):
    try:
        _value = self.config.get(f"{_section}", f"{_option}")
        return _value
    except Exception as e:
        print(f"{self.get_option.__name__}()\n{repr(e)}")
        return False
    
```

#### get_options

Returns a list of all options.

```python
def get_options(self, _section: str) -> (list | bool):
    try:
        return self.config.options(f"{_section}")
    except Exception as e:
        print(f"{self.get_sections.__name__}()\n{repr(e)}")
        return False
            
```

#### set_option

Set the value of a given option.

```python
def set_option(self, _section: str, _option: str, _new_value: str) -> bool:
    try:
        self.config.set(f"{_section}", f"{_option}", f"{_new_value}")
        return True
    except Exception as e:
        print(f"{self.set_option.__name__}()\n{repr(e)}")
        return False
      
```

#### add_option

Create a new config option.

```python
def add_option(self, _section: str, _new_option: str, _value: str) -> bool:
    try:
        if not self.option_exists(f"{_section}", f"{_new_option}"):
            self.config.set(f"{_section}", f"{_new_option}", f"{_value}")
            return True
        return False
    except Exception as e:
        print(f"{self.add_option.__name__}()\n{repr(e)}")
        return False

```

#### remove_option

Remove a configuration option.

```python
def remove_option(self, _section: str, _option: str) -> bool:
    try:
        self.config.remove_option(f"{_section}", f"{_option}")
        return True
    except Exception as e:
        print(f"{self.remove_option.__name__}()\n{repr(e)}")
        return False
        
```

#### option_exists

Check if a configuration option exists.

```python
def option_exists(self, _section: str, _option: str) -> bool:
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
        
```

#### section_exists

Check if a configuration section exists.

```python
def section_exists(self, _section: str) -> bool:
    try:
        if self.config.has_section(f"{_section}"):
            return True
        return False
    except Exception as e:
        print(f"{self.section_exists.__name__}()\n{repr(e)}")
        return False
        
```

#### add_section

Add a new configuration section.

```python
def add_section(self, _section: str) -> bool:   
    try:
        if not self.section_exists((f"{_section}")):
            self.config.add_section(f"{_section}")
            return True
        return False
    except Exception as e:
        print(f"{self.add_section.__name__}()\n{repr(e)}")
        return False

```

#### remove_section

Remove a configuration section.

```python
def remove_section(self, _section: str) -> bool:
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

```

#### get_sections

Returns a list of all sections.

```python
def get_sections(self) -> (list | bool):
    try:
        return self.config.sections()
    except Exception as e:
        print(f"{self.get_sections.__name__}()\n{repr(e)}")
        return False
       
```

#### set_default_section

Set the name of the defaults section.

```python
def set_default_section(self, _section: str) -> bool:
    try:
        if len(_section) != 0:
            self.config.default_section = _section
            return True
        return False
    except Exception as e:
        print(f"{self.set_default_section.__name__}()\n{repr(e)}")
        return False
        
```

#### get_default_option_values

Returns a dictionary containing the default values from the parser.
The dictionary represents the options and their corresponding default 
values present in the default section.

```python
def get_default_option_values(self) -> (dict | bool):
    """   
    """
    try:
        return self.config.defaults()
    except Exception as e:
        print(f"{self.get_default_option_values.__name__}()\n{repr(e)}")
        return False
        
```

## [Contributing](#contributing)

If you have any feature requests, suggestions or general questions you can reach me via any of the
methods listed below in the [Contacts](#contacts) section.

---

## [Security](#security)

### Reporting a vulnerability or bug?

**Do not submit an issue or pull request**: A general rule of thumb is to never publicly report bugs or vulnerabilities because you might inadvertently reveal it to unethical people who may use it for bad. Instead, you can email me directly at: [paulmccarthy676@gmail.com](mailto:paulmccarthy676@gmail.com). I will deal with the issue privately and submit a patch as soon as possible.

---

## [Contacts](#contacts)

**Author:** Paul M.

- Email: [paulmccarthy676@gmail.com](mailto:paulmccarthy676@gmail.com)
- Github: [https://github.com/happycod3r](https://github.com/happycod3r)
- Linkedin: [https://www.linkedin.com/in/paul-mccarthy-89165a269/]( https://www.linkedin.com/in/paul-mccarthy-89165a269/)
- Facebook: [https://www.facebook.com/paulebeatz]( https://www.facebook.com/paulebeatz)

---
