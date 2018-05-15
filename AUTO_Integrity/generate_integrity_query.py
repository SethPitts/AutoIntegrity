import pandas as pd

# get various sections of integrity file from excel

checks_in_template_df = pd.read_excel('CTN_0067_Integrity_Checks.xlsx', sheet_name='CHECKS_IN_TEMPLATE')
comments_df = pd.read_excel('CTN_0067_Integrity_Checks.xlsx', sheet_name='COMMENTS')
req_name_df = pd.read_excel('CTN_0067_Integrity_Checks.xlsx', sheet_name='REQ_NAME')
file_name_df = pd.read_excel('CTN_0067_Integrity_Checks.xlsx', sheet_name='FILE_NAMES')
temp_var_df = pd.read_excel('CTN_0067_Integrity_Checks.xlsx', sheet_name='TEMP_VARS')
checks_df = pd.read_excel('CTN_0067_Integrity_Checks.xlsx', sheet_name='CHECKS')

# Get Checks present in template
checks_in_template = checks_in_template_df.CHECK_NAME
for check_name in checks_in_template:
    with open('{}.REQ'.format(check_name), 'w') as req_file:
            # Write Comments
            filtered_comments_df = comments_df[(comments_df.CHECK_NAME == check_name)]  # Filter data frame by check
            comments = filtered_comments_df.Comment_Text
            comment_template = "COMMENT  {}\n"
            for comment in comments:
                req_file.write(comment_template.format(comment))

            # write new line
            req_file.write("\n")

            # Write REQ-NAME
            filtered_req_name_df = req_name_df[(req_name_df.CHECK_NAME == check_name)]  # Filter data frame by check
            req_name_template = "REQ-NAME {}{}\n"
            for idx, req_info in filtered_req_name_df.iterrows():
                req_name = req_info.loc['REQ_NAME']
                padded_spaces = " " * (10 - len(req_name))
                retain_delete = req_info.loc['RETAIN_DELETE']
                req_file.write(req_name_template.format(req_name + padded_spaces, retain_delete))

            # Write FILE-NAME
            filtered_file_name_df = file_name_df[(file_name_df.CHECK_NAME == check_name)]  # Filter data frame by check
            file_name_template = "FILE-{}{}{}\n"
            for idx, file_info in filtered_file_name_df.iterrows():
                file_num = file_info.loc['FILE_NUM']
                file_name = file_info.loc['FILE_NAME']
                padded_spaces_1 = " " * (10 - len(file_name))
                padded_spaces_2 = " " * (4 - len(str(file_num)))
                key_fields = " ".join(file_info.loc['KEY_FIELDS'].split(","))
                req_file.write(file_name_template.format(str(file_num) + padded_spaces_2, file_name + padded_spaces_1, key_fields))

            # New Line
            req_file.write('\n')

            # Write TEMPFILES
            filtered_temp_var_df = temp_var_df[(temp_var_df.CHECK_NAME == check_name)]  # Filter data frame by check
            req_file.write('TEMPBEG\n')
            var_template = "{}   {}{}\n"

            for idx, var_info in filtered_temp_var_df.iterrows():
                var_name = var_info.loc['VAR_NAME']
                var_type = var_info.loc['TYPE']
                var_code = var_info.loc['CODE']
                req_file.write(var_template.format(var_name, var_type, var_code))

            req_file.write("TEMPEND\n\n")

            # Write CHECKS
            filtered_checks_df = checks_df[(checks_df.CHECK_NAME == check_name)]  # Filter data frame by check
            check_line1_template = "{} {}{} {} {}{}{}\n"

            for idx, var_info in filtered_checks_df.iterrows():
                edit_check_def = var_info.loc['EDIT_CHECK_DEFINITION_LINE']
                edit_check_name = var_info.loc['EDIT_CHECK_NAME']
                legal_illegal = var_info.loc['LEGAL_ILLEGAL']
                missing_records = var_info.loc['MISSING_RECORDS']
                error_code = var_info.loc['ERROR_CODE']
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
                check_code = var_info.loc['CODE']
                req_file.write(code_template.format(check_code))




