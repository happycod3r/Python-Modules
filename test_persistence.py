import persistence
import os

def persistence_module_test() -> bool:
    """
    This is a general test for the persistence module set up in such a
    way that all of the Persistence class methods will run one after
    the other in a logical way.
    
    The process will start at the creation of the config file and directory 
    and go all through the different steps in between to end with the deletion of 
    the config file and directory.
    
    For the test to pass all 20 steps should return and print either 'True' or
    the value that it is supposed to return.
    
    You can also use this or the README as a reference as to the proper order
    to call the class methods.
    
    """
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

    try:

        config = persistence.Persistence(f"{os.path.join(CURRENT_PATH, 'config')}", f"{os.path.join(CURRENT_PATH, 'config/test.conf')}")

        print("1)", config.create_config_dir())
        print("2)", config.create_config_file())

        print("3)", config.open_config())
        print("4)", config.add_section("user"))
        print("5)", config.add_option("user", "name", "Paul"))
        print("6)", config.save_config())

        print("7)", config.open_config())
        print("8)", config.set_option("user", "name", "Tia"))
        print("9)", config.save_config())

        if config.section_exists("user"):
            print("10)", "User section exists.")

        if config.option_exists("user", "name"):
            print("11)", "Option exists.")
            
        print("12)", config.get_config_dir_path())
        print("13)", config.dump_config_to_output())
        print("14)", config.get_options("user"))
        print("15)", config.get_sections())
        print("16)", config.read_config())

        if config.get_option("user", "name") == "Tia":
            print("17)", config.remove_option("user", "name"))
            print("18)", config.remove_section("user"))

        print("19)", config.delete_config_file())
        print("20)", config.delete_config_dir())
        
        return True
    except Exception as e:
        print(repr(e))
        return False

if persistence_module_test(): print("\n##### Test passed! #####\n")
else: print("\n##### Test failed! #####\n")

