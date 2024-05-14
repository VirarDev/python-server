import shutil
import os
import subprocess
import time

root_dir = os.getcwd().replace("\\", "/")
storage = root_dir+"/storage/"


def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Command output:\n", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Command failed with error:", e)
        print("Error output:\n", e.stderr)
        return e.stderr


def write_update(user, path, data):
    stack = [(path, data)]
    while stack:
        current_path, current_data = stack.pop()
        for key, value in current_data.items():
            new_path = (current_path+"/"+key) if current_path else key
            if isinstance(value, dict):
                stack.append((new_path, value))
            else:
                file_path = storage + user+"/" + new_path + ".txt"
                if (isinstance(value, str)):
                    value = '"' + value
                elif (isinstance(value, bool)):
                    if (value == True):
                        value = "T"
                    else:
                        value = "F"
                os.remove(file_path)
                with open(file_path, 'wb') as file:
                    file.write(str(value).encode('utf-8'))


def write(user, path, data):
    stack = [(path, data)]
    while stack:
        current_path, current_data = stack.pop()
        for key, value in current_data.items():
            new_path = (current_path+"/"+key) if current_path else key
            if isinstance(value, dict):
                stack.append((new_path, value))
            else:
                file_path = storage + user+"/" + new_path + ".txt"
                if (isinstance(value, str)):
                    value = '"' + value
                elif (isinstance(value, bool)):
                    if (value == True):
                        value = "T"
                    else:
                        value = "F"
                os.makedirs(storage + user + "/" + current_path, exist_ok=True)
                with open(file_path, 'wb') as file:
                    file.write(str(value).encode('utf-8'))


def cnvt_to_type(data):
    resp = data
    typ = data[0]
    if (typ == '"'):
        resp = data[1:]
    elif (typ == "["):
        resp = eval(data)
    elif (typ == "T"):
        resp = True
    elif (typ == "F"):
        resp = False
    else:
        resp = float(data)
    return resp


def read(user, path, isCollection):
    if (isCollection == True):
        try:
            data = dict()
            data["_COLLECTIONS"] = []
            with os.scandir(storage+user+"/"+path) as entries:
                for entry in entries:
                    if entry.is_file():
                        with open(entry, 'rb') as file:
                            txt = file.read().decode('utf-8')
                            resp = ""
                            try:
                                resp = cnvt_to_type(txt)
                            except:
                                resp = txt
                            data[entry.name[:-4]] = resp

                    elif entry.is_dir():
                        data["_COLLECTIONS"].append(entry.name)
            return data
        except OSError as e:
            return f"Error : {e}"
    else:
        with open(storage+user+"/"+path + ".txt", 'rb') as f:
            data = f.read()
            try:
                resp = {
                    "data": cnvt_to_type(data)
                }
                return resp
            except:
                return data


def remove(user, path, isCollection):
    path_del = storage+user+"/"+path
    if isCollection:
        try:
            shutil.rmtree(path_del)
        except OSError as e:
            return "Error : "+str(e)
    else:
        try:
            os.remove(path_del + ".txt")
        except OSError as e:
            return "Error : "+str(e)
    return "ok"


def get(body):
    try:
        user = body["USER"]
        if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
            return "Invalid User"
        path = body["PATH"]
        isCollection = body["IS_COLLECTION"]
        if (not isinstance(isCollection, bool)):
            return "Invalid IS_COLLECTION only True or False"
        return read(user, path, isCollection)
    except Exception as e:
        return "Error : "+str(e)


def update(body):
    try:
        user = body["USER"]
        if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
            return "Invalid User"
        path = body["PATH"]
        data = body["DATA"]
        write_update(user, path, data)
        return "ok "
    except Exception as e:
        return "Error : "+str(e)


def store(body):
    try:
        user = body["USER"]
        if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
            return "Invalid User"
        path = body["PATH"]
        data = body["DATA"]

        os.makedirs(root_dir+"/storage/"+user+"/"+path, exist_ok=True)

        write(user, path, data)
        # current_time_in_ms = int(time.time() * 1000)

        # json_path = root_dir+"/jsons/"+str(current_time_in_ms)+".json"
        # with open(json_path, 'w', encoding='utf-8') as file:
        #     file.write(str(data))
        # # return root_dir+"/Cpp/store_master.exe "+path+" "+json_path
        # # res = execute_command(root_dir+"/Cpp/store_master.exe "+path+" "+json_path)

        # subprocess.run([root_dir+'/Cpp/store_master',
        #                path, root_dir+'/jsons/'+str(current_time_in_ms)+'.json'])

        return "ok "
    except Exception as e:
        return "Error : "+str(e)


def delete(body):
    try:
        user = body["USER"]
        if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
            return "Invalid User"
        path = body["PATH"]
        isCollection = body["IS_COLLECTION"]
        if (not isinstance(isCollection, bool)):
            return "Invalid IS_COLLECTION only True or False"
        return remove(user, path, isCollection)
    except Exception as e:
        return "Error : "+str(e)
