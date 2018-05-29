import datetime
import pandas as pd
from text_formatter import format_by_charater_length


def Create_Req_Files_From_Tracker():
    integrity_tracker_df = pd.read_excel('CTN-0067 Integrity Tracker2.xlsx', sheet_name='0067 Specific Checks')
    # Create DF of only reqs that are in the status []
    active_integrity_tracker_df = integrity_tracker_df[integrity_tracker_df.Status == 'Ready For Review']
    # Get reqs present in template`
    reqs_in_template = active_integrity_tracker_df.File_Name
    # Create a req file for each req that has the correct status
    for req_file_name in reqs_in_template:
        current_req_df = active_integrity_tracker_df[active_integrity_tracker_df.File_Name == req_file_name]
        with open('{}.REQ'.format(req_file_name), 'w') as req_file:
            today = str(datetime.datetime.date(datetime.datetime.now()))
            # Write Comment header based on the forms in the req
            form_1 = current_req_df.FORM_1.iloc[0]
            form_1_key_fields = current_req_df.FORM_1_Key_Fields.iloc[0]
            form_2 = current_req_df.FORM_2.iloc[0]
            form_2_key_fields = current_req_df.FORM_2_Key_Fields.iloc[0]
            # Req with only 1 form
            if type(form_2) == float:  # it will be a float if it's empty
                forms_in_req = {form_1: form_1_key_fields}
                comment_string = "COMMENT THIS IS A REQ CREATED FOR {}\nCOMMENT Created on {} automatically\n".format(
                    form_1, today)
            # Req with 2 forms
            else:
                forms_in_req = {form_1: form_1_key_fields,
                                form_2: form_2_key_fields
                                }
                comment_string = "COMMENT THIS IS A REQ CREATED FOR {}/{}\nCOMMENT Created on {} automatically\n".format(
                    form_1, form_2, today)
            req_file.write(comment_string)
            # write new line
            req_file.write("\n")

            # Write REQ-NAME to req file
            req_name = req_file_name  # Filter data frame by check
            req_name_template = "REQ-NAME {}{}\n"
            padded_spaces = " " * (10 - len(req_name))  # Used to place text at correct column line
            retain_delete = 'RETAIN'  # We always retrain
            req_file.write(req_name_template.format(req_name + padded_spaces, retain_delete))

            # Write FILE-NAME to req file
            file_name_template = "FILE-{}{}{}\n"
            for form_num, form in enumerate(forms_in_req):
                file_num, file_name = form_num + 1, form
                key_fields = forms_in_req[form]
                padded_spaces_1 = " " * (10 - len(file_name))  # Used to place text at correct column line
                padded_spaces_2 = " " * (4 - len(str(file_num)))
                key_fields = key_fields.replace(",", " ")
                req_file.write(
                    file_name_template.format(str(file_num) + padded_spaces_2, file_name + padded_spaces_1, key_fields))

            # New Line
            req_file.write('\n')

            # Write TEMPFILES to req file
            # Variables are separated by ":"
            temp_variables = current_req_df.Temp_Files.iloc[0].split(
                ":")  # separated by -  # Filter data frame by check
            req_file.write('TEMPBEG\n')
            var_template = "{}   {}{}\n"

            for temp_var in temp_variables:
                #  teamp variable parts are separated by "|"
                var_name, var_type, var_code = temp_var.split("|")
                req_file.write(var_template.format(var_name, var_type, var_code))
            req_file.write("TEMPEND\n\n")

            # Write CHECKS to file
            filtered_checks_df = current_req_df[
                (current_req_df.File_Name == req_file_name)]  # Filter data frame by check
            check_line1_template = "{} {}{} {} {}{}{}\n"

            for idx, var_info in filtered_checks_df.iterrows():
                edit_check_def = var_info.loc['EDIT_CHECK_DEFINITION_LINE']
                edit_check_name = var_info.loc['Check_Name']
                legal_illegal = var_info.loc['LEGAL_ILLEGAL']
                missing_records = var_info.loc['MISSING_RECORDS']
                error_code = var_info.loc['Error_Code']
                check_comment = var_info.loc['CHECK_COMMENT']
                padded_spaces_1 = " " * (15 - len(edit_check_name))
                padded_spaces_2 = " " * (50 - len(check_comment))
                padded_spaces_3 = " " * (6 - len(error_code))
                check_type = var_info.loc['TYPE']
                req_file.write(check_line1_template.format(edit_check_def, edit_check_name + padded_spaces_1,
                                                           legal_illegal, missing_records, error_code + padded_spaces_3,
                                                           check_comment + padded_spaces_2, check_type))

                # Write Code
                code_template = "  {}\n\n"
                check_code = var_info.loc['Check']
                req_file.write(code_template.format(format_by_charater_length(60, check_code)))


Create_Req_Files_From_Tracker()
