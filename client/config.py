'''
Created on Jan 12, 2016

@author: Connor
'''

import pkgutil, os, traceback, yaml
import client.modules.api_library as api_library
import client.settings as settings

def safe_input(prompt, require=False):
    answer = ''
    if require:
        confirm = 'N'
        while (len(confirm) < 1 or confirm.upper()[0] is not 'Y'):
            answer = input(prompt)
            if not answer:
                print("\n~ Please enter a valid value")
                continue
            print("\n~ Input:", answer)
            confirm = input("~ Confirm (Y / N): ")
            print()
    else:
        answer = input(prompt)
        print()
    return answer

def block_print(title):
    if not title:
        title = "(empty)"
    length = len(title)+10
    print("#"*length)
    print("#" + " "*(length-2) + "#")
    print("#    " + title + "    #")
    print("#" + " "*(length-2) + "#")
    print("#"*length + "\n")

def generate():
    block_print("USER CONFIG FILE GENERATOR")
    print("~ Please let me learn some things about you :)\n")
    print("~ All of the following is optional, of course.\n")
    config_info = {}

    for finder, name, _ in pkgutil.iter_modules(api_library.__path__):
        try:
            api = finder.find_module(name).load_module(name)
            if hasattr(api, 'config_generator'):
                block_print(name.replace("_", " ").upper())
                api_info = api.config_generator()
                if api_info:
                    if name is "user_api":
                        config_info += api_info
                    else:
                        config_info[name] += api_info
        except Exception as e:
            print(traceback.format_exc())
            print('\n~ Error loading \''+name+'\' '+str(e))
    file_loc = os.path.join(settings.USERS_DIR, config_info['username']+".yml")
    print("~ Writing to:", file_loc)
    with open(file_loc, 'w') as f:
        yaml.dump(config_info, f, default_flow_style=False)
    print("~ Success! Feel free to boot me up now.")
