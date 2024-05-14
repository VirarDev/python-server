import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

TABLE_NAME = get_table_name()

import functions.sql.basics as base

get = lambda body:base.get(TABLE_NAME,body)
count = lambda body:base.count(TABLE_NAME,body)
store = lambda body:base.store(TABLE_NAME,body)
update = lambda body:base.update(TABLE_NAME,body)
delete = lambda body:base.delete(TABLE_NAME,body)
run = lambda body:base.run(TABLE_NAME,body)
def get_columns():return base.get_columns(TABLE_NAME)
def pragma():return base.pragma(TABLE_NAME)


def cv_details_get(body):
    candidate_id = body["ID"]
    
    cv = base.get(TABLE_NAME,{
        "COLUMNS":"*",
        "CONDITION": f"WHERE id = '{candidate_id}'"
    },True)
    
    cv[0] = column_name_conversion(cv[0])

    Cv_Column_Names = cv[0]
    if(len(cv) == 1):
        return None
    Cv_Details = cv[1]

    Comid = Cv_Details[Cv_Column_Names.index("Comid")]
    Jobid = Cv_Details[Cv_Column_Names.index("Jobid")]
    Assigned_To_UID = Cv_Details[Cv_Column_Names.index("ASSIGNED_TO")]

    Company_Name = base.get("COMPANY",{
        "COLUMNS":"Name",
        "CONDITION":f"WHERE id='{Comid}'"
    },True)[1][0]

    Job_Role_Name = ""
    try:
        Job_Role_Name = base.get("JOBS",{
            "COLUMNS":"Name",
            "CONDITION":f"WHERE id='{Jobid}'"
        },True)[1][0]
    except:
        Job_Role_Name = "(Role Not Found)"

    Assigned_To_Detail = base.get("USERS",{
        "COLUMNS":"Name,Mail",
        "CONDITION":f"WHERE id='{Assigned_To_UID}'"
    },True)

    Assigned_To_Name = None
    Assigned_To_Email = None

    try:
        Assigned_To_Detail = Assigned_To_Detail[1]

        Assigned_To_Name = Assigned_To_Detail[0]
        Assigned_To_Email = Assigned_To_Detail[1]
    except:
        pass

    Cv_Details_Dict = {}
    for i in range(len(Cv_Details)):
        Cv_Details_Dict[Cv_Column_Names[i]] = Cv_Details[i]

    return base.js({
        "Company_Name":Company_Name,
        "Job_Role_Name":Job_Role_Name,
        "Assigned_To_Name":Assigned_To_Name,
        "Assigned_To_Email":Assigned_To_Email,
        "Cv_Column_Names":Cv_Column_Names,
        "Cv_Details":Cv_Details_Dict,
    })

def search(body):
    try:
        rows = base.get(TABLE_NAME,body,True)
        rows[0] = column_name_conversion(rows[0])
        return base.js(rows)
    except Exception as e:
        return "Error : "+str(e)
    


def column_name_conversion(columns):
    try:
        for i in range(len(columns)) :    
            ind = BASIC_column_name_lower_case.index(columns[i])
            columns[i] = BASIC_column_name[ind]
        return columns
    except:
        a = 0
        a+=23
        return None

BASIC = { 
    "POSITION_SHARED_DATEMS": "int",
    "EXPERIENCE_IN_SAN": "int",
    "CV_SUBMISSION_DATEMS": "int",
    "BENEFITS": "str",
    "DETAIL_PEOPLE_REPORTING": "str",
    "PhaseMS2": "int",
    "ASSIGNED_TO": "str",
    "SelectedPhaseIndex": "int",
    "STATUS": "str",
    "PROFILE_URL": "str",
    "PhaseMS1": "int",
    "QUALIFICATION": "str",
    "PhaseMS8": "int",
    "CURRENTLY_WORKS_WITH": "str",
    "MONITORING_TOOLS": "str",
    "PEOPLE_MANAGEMENT_EXPERIENCE": "str",
    "CURRENT_COMPANY": "str",
    "MANAGERIAL_YEARS_OF_EXPERIENCE": "str",
    "KEY_SYSTEMS_EXPERIENCE": "str",
    "GRADE_FITMENT": "str",
    "EMPLOYMENT_GAP": "str",
    "Jobid": "str",
    "Phase2": "str",
    "RESPONSIBILITY": "str",
    "TIME_SLOT": "str",
    "GRADE": "str",
    "HIRING_LOCATION": "str",
    "REMARKS": "str",
    "WINDOWS_AND_VMWARE": "str",
    "id": "str",
    "C_CTC_BREAKUPS": "str",
    "Phase6": "str",
    "REASON_FOR_CHANGE": "str",
    "OUR_OFFERS": "str",
    "SCRIPTING": "str",
    "FeildType": "str",
    "SelectedPhaseIndex0": "int",
    "Phase1": "str",
    "PhaseMS6": "int",
    "NO_PEOPLE_REPORTING": "str",
    "RELEVANT_YEARS_OF_EXPERIENCE": "int",
    "CONFIGURATION": "str",
    "YEAR_OF_EXPERIENCE": "int",
    "DATE_OF_SHARINGMS": "int",
    "GENDER": "str",
    "SERVER": "str",
    "E_CTC": "int",
    "CURRENT_COMPANY_AND_WORKING_SINCE": "str",
    "LINUX": "str",
    "CERTIFICATION": "str",
    "PhaseMS00": "int",
    "Comid": "str",
    "YEAR_OF_PASSING": "int",
    "E_CTC_BREAKUPS": "str",
    "SKILLS": "str",
    "CAREER_GAP": "str",
    "TEAM": "str",
    "C_CTC": "int",
    "DIVERSITY": "str",
    "CBSI_POSITION_ID": "str",
    "POSITION_SHARED_DATE": "str",
    "CANDIDATE_ID": "str",
    "CLOUD": "str",
    "Phase00": "str",
    "TICKETING_TOOL": "str",
    "CV_SUBMISSION_DATE": "str",
    "TOWER_LEAD": "str",
    "COUNTER_OFFER": "str",
    "OFFER_BREAKUPS": "str",
    "AUTOMATION": "str",
    "RESUME_URL": "str",
    "DATE_OF_SHARING": "str",
    "PhaseMS0": "int",
    "VARIABLE_PAY": "str",
    "CANDIDATE_NAME": "str",
    "COMMENTS": "str",
    "TECHNOLOGIES_WORKED_ON": "str",
    "WINDOWS": "str",
    "ORG_WORKED_WITH": "str",
    "Phase0": "str",
    "CURRENT_DESIGNATION": "str",
    "REQ_ID": "str",
    "CONTACT_NO": "str",
    "CURRENT_FIXED": "str",
    "NOTICE_PERIOD": "str",
    "DATABASE": "str",
    "POSITION_CODE": "str",
    "DATACENTRE_MANAGEMENT": "str",
    "VENDOR_NAME": "str",
    "TOTAL_JOB_CHANGES": "int",
    "Phase8": "str",
    "CURRENT_LOCATION": "str",
    "EMAIL_ID": "str",
    "STORAGE": "str",
    "CATEGORY": "str",
    "Phase5": "str",
    "PhaseMS5": "int",
    "PhaseMS7": "int",
    "Phase7": "str",
    "PhaseMS21": "int",
    "SelectedPhaseIndex2": "int",
    "Phase21": "str",
    "Phase4": "str",
    "PhaseMS4": "int",
    "CURRENT_EMPLOYER": "str",
    "PhaseMS22": "int",
    "Phase22": "str",
    "Phase20": "str",
    "PhaseMS20": "int",
    "ResonForDeclined": "str",
    "Phase3": "str",
    "PhaseMS3": "int",
    "Phase23": "str",
    "PhaseMS23": "int",
    "PhaseMS12": "int",
    "SelectedPhaseIndex1": "int",
    "Phase12": "str",
    "PhaseMS10": "int",
    "Phase10": "str",
    "SOURCED_DATEMS": "int",
    "SOURCED_DATE": "str",
    "Phase11": "str",
    "PhaseMS11": "int",
    "PhaseMS24": "int",
    "Phase24": "str",
    "CREATED_BY": "str",
    "WE_OFFERED": "str",
    "Phase04": "str",
    "PhaseMS04": "int",
    "PhaseMS02": "int",
    "Phase02": "str",
    "PhaseMS01": "int",
    "Phase01": "str",
    "PhaseMS03": "int",
    "Phase03": "str",
    "PhaseMS13": "int",
    "Phase13": "str"
}

BASIC_column_name = [x for x in BASIC.keys()]
BASIC_column_name_lower_case = [x.lower() for x in BASIC.keys()]