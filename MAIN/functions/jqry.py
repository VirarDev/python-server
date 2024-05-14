import os
from flask import send_file

storage = os.getcwd().replace("\\", "/")+"/storage/"


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


def condition(c_val, condition, val):
    col_val = ""
    try:
        col_val = cnvt_to_type(c_val)
    except:
        col_val = c_val

    if (condition == "$equal"):
        if (isinstance(col_val, float)):
            return float(val) == col_val
        elif (isinstance(col_val, bool)):
            if (val == "T"):
                return col_val == True
            elif (val == "F"):
                return col_val == False
            else:
                return False
        elif (isinstance(col_val, str)):
            return col_val == str(val[1:-1])
        else:
            return col_val == val
    elif (condition == "$not"):
        if (isinstance(col_val, float)):
            return float(val) != col_val
        elif (isinstance(col_val, bool)):
            if (val == "T"):
                return col_val != True
            elif (val == "F"):
                return col_val != False
            else:
                return False
        elif (isinstance(col_val, str)):
            return col_val != str(val[1:-1])
        else:
            return col_val != val
    elif (condition == "$less"):
        if (isinstance(col_val, float)):
            return float(val) >= float(col_val)
        else:
            return False
    elif (condition == "$great"):
        if (isinstance(col_val, float)):
            return float(val) <= float(col_val)
        else:
            return False
    elif (condition == "$contain"):
        if (isinstance(col_val, list) or isinstance(col_val, str)):
            if (val[0] == "'"):
                return str(val[1:-1]) in col_val
            elif (val[0] == 'T'):
                return True in col_val
            elif (val[0] == 'F'):
                return False in col_val
            else:
                return float(val) in col_val
        else:
            return False
    elif (condition == "$not_contain"):
        if (isinstance(col_val, list) or isinstance(col_val, str)):
            if (val[0] == "'"):
                return str(val[1:-1]) not in col_val
            elif (val[0] == 'T'):
                return True not in col_val
            elif (val[0] == 'F'):
                return False not in col_val
            else:
                return float(val) not in col_val
        else:
            return False
    else:
        return False


def evaluate_query(tokens, data_path):
    i = 0
    end = len(tokens)
    bi_qry = []
    while i < end:
        token = tokens[i]
        if (token in ["$(", "$)"]):
            if (token == "$("):
                j = i+1
                b = 0
                while True:
                    tk = tokens[j]
                    if (tk == "$("):
                        b += 1
                    if (tk == "$)"):
                        if (b == 0):
                            break
                        b -= 1
                    j += 1
                bi_qry.append(evaluate_query(tokens[i+1:j], data_path))
                i = j

        elif (token == "$and" or token == "$or"):
            bi_qry.append(token)
        else:
            col_name = token
            cond = tokens[i+1]
            val = tokens[i+2]
            col_val = None
            try:
                with open(data_path+"/"+col_name+".txt", 'rb') as file:
                    col_val = file.read().decode('utf-8')
                    bi_qry.append(condition(col_val, cond, val))
            except:
                bi_qry.append(False)
            i += 2
        i += 1

    result = bi_qry[0]

    for i in range(1, len(bi_qry), 2):
        operator = bi_qry[i]
        operand = bi_qry[i + 1]

        if operator == '$and':
            result = result and operand
        elif operator == '$or':
            result = result or operand

    return result


def read_cols(col_names, path):
    data = dict()
    if (col_names == "*"):
        with os.scandir(path) as entries:
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
    else:
        for col in col_names:
            try:
                with open(path+"/"+col+".txt", 'rb') as file:
                    data[col] = cnvt_to_type(file.read().decode('utf-8'))
            except:
                data[col] = None
    return data


def qry_select(user, path, where, select):
    query = where.split(" ")
    try:
        with open(storage+user+"_output.json", 'wb') as output_file:
            data = []

            if (select != ""):
                if (select != "*"):
                    select = select.split(",")
                data = dict()
                output_file.write('{'.encode('utf-8'))
            else:
                output_file.write('['.encode("utf-8"))

            q_path = storage+user+"/"+path
            with os.scandir(q_path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        # st = str(int(time.time() * 1000))
                        if (evaluate_query(query, q_path+"/"+entry.name) == True):
                            if (select == ""):
                                # data.append(entry.name)
                                output_file.write(
                                    (entry.name + ',').encode("utf-8"))
                            else:
                                # data[entry.name] = read_cols(select, q_path+"/"+entry.name)
                                output_file.write((entry.name + ':' + str(read_cols(
                                    select, q_path+"/"+entry.name))).encode("utf-8"))
                        # end = str(int(time.time() * 1000))
                        # time_take.append(entry.name+" - "+st+" to "+end)
            if (select != ""):
                output_file.write('}'.encode("utf-8"))
            else:
                output_file.write(']'.encode("utf-8"))
            return send_file(open(storage+user+"_output.json", 'rb'), as_attachment=True, mimetype='text/text', download_name='output_file.json')

    except OSError as e:
        return f"Error : {e}"


def qry_update(user, path, where, data_to_update):
    query = where.split(" ")
    try:
        q_path = storage+user+"/"+path
        with os.scandir(q_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    if (evaluate_query(query, q_path+"/"+entry.name) == True):
                        for item, value in data_to_update.items():
                            try:
                                os.remove(q_path+"/"+entry.name +
                                          "/"+item+".txt")
                            except:
                                pass
                            if (isinstance(value, str)):
                                value = '"' + value
                            elif (isinstance(value, bool)):
                                if (value == True):
                                    value = "T"
                                else:
                                    value = "F"
                            with open(q_path+"/"+entry.name +
                                      "/"+item+".txt", "wb") as file:
                                file.write(str(value).encode('utf-8'))

    except OSError as e:
        return f"Error : {e}"


def get(body):
    try:
        user = body["USER"]
        if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
            return "Invalid User"
        path = body["PATH"]
        where = body["WHERE"]
        try:
            select = body["SELECT"]
        except:
            select = ""
        return qry_select(user, path, where, select)
    except Exception as e:
        return "Error : "+str(e)


def update(body):
    try:
        user = body["USER"]
        if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
            return "Invalid User"
        path = body["PATH"]
        where = body["WHERE"]
        data = body["DATA"]
        qry_update(user, path, where, data)
        return "ok"
    except Exception as e:
        return "Error : "+str(e)


"""

test equal True and (test2 less 5 or test3 not demo)

"""
