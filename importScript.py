import pandas as pd
from datetime import datetime

# Read the Excel file into a pandas DataFrame
data = pd.read_excel('./Regulations for Initial Import.xlsx', sheet_name='Sheet1')

max_rows = data.shape[0]

reg_id = 1 # for regulation 1

# -- POLICY table --

insert_policy_string = '''INSERT INTO POLICY (POL_ID,
                    POL_NUMBER,
                    POL_TITLE,
                    POL_VERSION_NUMBER,
                    POL_STORAGE_LINK,
                    POL_NOTES)
VALUES (1,
       'Policy 1',
       'University Non-discrimination Policy',
       3,
       NULL,
       'Waiting on federal regulations expected May 2023 to update. Sherri would like to combine this policy with the ADA accommodation policy at that time');''' + '\n\n'
policy_id = 2
initial_policy_name = data.iloc[1][0]
column_p = 1
row_p = 1
while row_p < max_rows:
    current_policy_name = str(data.iloc[row_p][0])
    if current_policy_name != 'nan' and current_policy_name != str(initial_policy_name):
        pol_version_num = data.iloc[row_p][column_p+2] if str(data.iloc[row_p][column_p+2]) != 'nan' else 'NULL'
        pol_notes = f'''"{str(data.iloc[row_p][column_p+7])}"''' if str(data.iloc[row_p][column_p+7]) != 'nan' else 'NULL'
        insert_policy = f'''INSERT INTO POLICY (POL_ID, POL_NUMBER, POL_TITLE, POL_VERSION_NUMBER, POL_STORAGE_LINK, POL_NOTES) VALUES ({policy_id}, "{current_policy_name}", "{current_policy_name}", {pol_version_num}, NULL, {pol_notes});'''
        insert_policy_string = insert_policy_string + insert_policy + '\n\n'
        policy_id = policy_id + 1

    row_p = row_p + 1

with open('insertStatementsComplete.sql', 'w') as file:
    file.write('-- POLICY table --\n\n')
    file.write(insert_policy_string)


# -- REGULATION_CLASSIFICATION table --
with open('insertStatementsComplete.sql', 'a') as file:
    file.write('''-- REGULATION_CLASSIFICATION table
    
INSERT INTO REGULATION_CLASSIFICATION (REG_CLASSIFICATION_ID,
                                        REG_CLASSIFICATION_NAME)
VALUES (1, 'Rule'),
    (2, 'Procedure'),
    (3, 'Guideline'),
    (4, 'Policy');''')

# -- REGULATION table --

policy_id = 1
insert_reg_string = ''
row_r = 1 # starting from 1st regulation
column_r = 1
initial_policy_name = data.iloc[1][0]
while row_r < max_rows:
    regulation_name = data.iloc[row_r][column_r]
    
    if str(regulation_name) != 'nan':
        regulation_title = data.iloc[row_r][column_r+1]
        reg_version_num = data.iloc[row_r][column_r+2] if str(data.iloc[row_r][column_r+2]) != 'nan' else 'NULL'

        current_policy_name = data.iloc[row_r][0]
        if str(current_policy_name) != 'nan' and str(current_policy_name) != str(initial_policy_name): 
            policy_id = policy_id + 1

        reg_status = f"'{str(data.iloc[row_r][column_r+3])}'" if str(data.iloc[row_r][column_r+3]) != 'nan' else 'NULL'
        reg_type = data.iloc[row_r][column_r+5]
        reg_classification_id = -1
        if str(reg_type) == 'Rule':
            reg_classification_id = 1
        elif str(reg_type) == 'Procedure':
            reg_classification_id = 2
        elif str(reg_type) == 'Guideline':
            reg_classification_id = 3
        elif str(reg_type) == 'Policy':
            reg_classification_id = 4
        reg_effective_date_xl = data.iloc[row_r][column_r+4]
        if str(reg_effective_date_xl) != 'nan':
            reg_effective_date = reg_effective_date_xl.strftime('%Y-%m-%d')
            reg_effective_date = f"'{reg_effective_date}'"
        else: 
            reg_effective_date = 'NULL'
        reg_notes = f'''"{str(data.iloc[row_r][column_r+7])}"''' if str(data.iloc[row_r][column_r+7]) != 'nan' else 'NULL'
        reg_interim_or_final = 'Interim' if str(data.iloc[row_r][column_r+8]) == 'Yes' else 'Final'
        reg_editorial_rev_yn = 1 if str(data.iloc[row_r][column_r+12]) != 'nan' else 0
        reg_rev_flag_yn = 1 if str(data.iloc[row_r][column_r+18]) == 'Yes' else 0
        is_reg_being_revised = 1 if str(data.iloc[row_r][column_r+30]) == 'Yes' else 0
        policy_name_of_reg = data.iloc[row_r][column_r-1]
        
        insert_regulation = f'''INSERT INTO REGULATION (REG_ID, REG_NUMBER, REG_TITLE, REG_VERSION_NUMBER, POL_ID, REG_CLASSIFICATION_ID, REG_STATUS, REG_EFFECTIVE_DATE, REG_METADATA, REG_LAST_REVIEW_DATE, REG_NOTES, REG_INTERIM_OR_FINAL, REG_EDITORIAL_REV_YN, REG_REV_FLAG_YN, REG_REV_FLAG_NOTES, REG_WEBSITE_LINK, IS_REG_BEING_REVISED, REG_STORAGE_LINK, DIRECT_DOCUMENT_LINK) VALUES ({reg_id}, "{regulation_name}", "{regulation_title}", {reg_version_num}, {policy_id}, {reg_classification_id}, {reg_status}, {reg_effective_date}, NULL, NULL, {reg_notes}, "{reg_interim_or_final}", {reg_editorial_rev_yn}, {reg_rev_flag_yn}, NULL, NULL, {is_reg_being_revised}, NULL, NULL);'''
        insert_reg_string = insert_reg_string + insert_regulation + '\n\n'
        
        reg_id = reg_id + 1
    
    row_r = row_r + 1

with open('insertStatementsComplete.sql', 'a') as file:
    file.write('\n\n-- REGULATION table --\n\n')
    file.write(insert_reg_string)

# -- CITATION_CLASSIFICATION table --
with open('insertStatementsComplete.sql', 'a') as file:
    file.write('''-- CITATION_CLASSIFICATION table
               
INSERT INTO CITATION_CLASSIFICATION (CITATION_CLASSIFICATION_ID,
                                    CITATION_CLASSIFICATION_NAME)
VALUES (1, 'Citations to USHE Policy'),
    (2, 'Citation to Utah law or Administrative Rules'),
    (3, 'Citation to federal law or regulations');
''')

# -- CITATION table --

reg_id = 1
insert_cit_string = ''
row_c_1 = 1
column_c_1 = 1
citation_classification_id = 1
citation_id = 1

while row_c_1 < max_rows:
    regulation_name = data.iloc[row_c_1][column_c_1]

    if(str(regulation_name) != 'nan'):
        row_c_2 = row_c_1
        column_c_2 = 21

        while column_c_2 < 24:
            citation_name = data.iloc[row_c_2][column_c_2]

            next_regulation_name = data.iloc[row_c_2][column_c_1]
            
            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif str(citation_name) == 'nan':
                citation_classification_id = citation_classification_id + 1
                column_c_2 = column_c_2 + 1
                row_c_2 = row_c_1 # reset
            else:
                insert_citation = f'''INSERT INTO CITATION (CITATION_ID, CITATION_NAME, CITATION_STORAGE_LINK, CITATION_CLASSIFICATION_ID, REG_ID, CITATION_NOTES)
                                VALUES ({citation_id}, "{citation_name}", NULL, {citation_classification_id}, {reg_id}, NULL);'''
                insert_cit_string = insert_cit_string + insert_citation + '\n\n'
                row_c_2 = row_c_2 + 1
                citation_id = citation_id + 1

        reg_id = reg_id + 1
        citation_classification_id = 1 # reset
    
    row_c_1 = row_c_1 + 1

with open('insertStatementsComplete.sql', 'a') as file:
    file.write('\n\n-- CITATION table --\n\n')
    file.write(insert_cit_string)
                            
# -- REGULATION_CITATION table --

reg_id = 1
insert_reg_cit_string = ''
row_rc_1 = 1
column_rc_1 = 1
citation_id = 1

while row_rc_1 < max_rows:
    regulation_name = data.iloc[row_rc_1][column_rc_1]

    if(str(regulation_name) != 'nan'):
        row_rc_2 = row_rc_1
        column_rc_2 = 21

        while column_rc_2 < 24:
            citation_name = data.iloc[row_rc_2][column_rc_2]
            next_regulation_name = data.iloc[row_rc_2][column_rc_1]
            
            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif str(citation_name) == 'nan':
                column_rc_2 = column_rc_2 + 1
                row_rc_2 = row_rc_1 # reset
            else:
                insert_reg_cit = f'''INSERT INTO REGULATION_CITATION (REG_ID, CITATION_ID) VALUES ({reg_id}, {citation_id});'''
                
                insert_reg_cit_string = insert_reg_cit_string + insert_reg_cit + '\n\n'

                row_rc_2 = row_rc_2 + 1
                citation_id = citation_id + 1

        reg_id = reg_id + 1
    
    row_rc_1 = row_rc_1 + 1

with open('insertStatementsComplete.sql', 'a') as file:
    file.write('\n\n-- REGULATION_CITATION table --\n\n')
    file.write(insert_reg_cit_string)

# -- STAKEHOLDER_CLASSIFICATION table --
with open('insertStatementsComplete.sql', 'a') as file:
    file.write('''-- STAKEHOLDER_CLASSIFICATION table -- \n
INSERT INTO STAKEHOLDER_CLASSIFICATION (STAKEHOLDER_CLASSIFICATION_ID,
                                        STAKEHOLDER_CLASSIFICATION_NAME)
VALUES (1, 'Policy Owner'),
    (2, 'Policy Officer'),
    (3, 'Contact Person');''')

# -- STAKEHOLDER and REGULATION_STAKEHOLDER table --

reg_id = 1
insert_stk_string = ''
insert_reg_stk_string = ''
stk_id = 1
row_stk_1 = 1 # starting from 1st regulation
column_stk_1 = 1
while row_stk_1 < max_rows:
    regulation_name = data.iloc[row_stk_1][column_stk_1]
    
    if str(regulation_name) != 'nan':

        # - policy owner - 
        row_stk_2 = row_stk_1
        while row_stk_2 < max_rows:
            next_regulation_name = data.iloc[row_stk_2][column_stk_1]

            policy_owner = str(data.iloc[row_stk_2][column_stk_1+9])

            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif policy_owner == 'nan':
                row_stk_2 = row_stk_2 + 1
                continue
            else:
                insert_policy_owner = f'''INSERT INTO STAKEHOLDER (STAKEHOLDER_ID, STAKEHOLDER_CLASSIFICATION_ID, STAKEHOLDER_NAME, STAKEHOLDER_POSITION, STAKEHOLDER_NOTES) VALUES ({stk_id}, 1, '{policy_owner}', NULL, NULL);'''
                insert_policy_owner_2 = f'''INSERT INTO REGULATION_STAKEHOLDER (REG_ID, STAKEHOLDER_ID) VALUES ({reg_id}, {stk_id});'''
                insert_stk_string = insert_stk_string + insert_policy_owner + '\n\n'
                insert_reg_stk_string = insert_reg_stk_string + insert_policy_owner_2 + '\n\n'
                stk_id = stk_id + 1
                row_stk_2 = row_stk_2 + 1

        # - policy officer -
        row_stk_3 = row_stk_1
        while row_stk_3 < max_rows:
            next_regulation_name = data.iloc[row_stk_3][column_stk_1]

            policy_officer = str(data.iloc[row_stk_3][column_stk_1+10])

            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif policy_officer == 'nan':
                row_stk_3 = row_stk_3 + 1
                continue
            else:
                insert_policy_officer = f'''INSERT INTO STAKEHOLDER (STAKEHOLDER_ID, STAKEHOLDER_CLASSIFICATION_ID, STAKEHOLDER_NAME, STAKEHOLDER_POSITION, STAKEHOLDER_NOTES) VALUES ({stk_id}, 2, '{policy_officer}', NULL, NULL);'''
                insert_policy_officer_2 = f'''INSERT INTO REGULATION_STAKEHOLDER (REG_ID, STAKEHOLDER_ID) VALUES ({reg_id}, {stk_id});'''
                insert_stk_string = insert_stk_string + insert_policy_officer + '\n\n'
                insert_reg_stk_string = insert_reg_stk_string + insert_policy_officer_2 + '\n\n'
                stk_id = stk_id + 1
                row_stk_3 = row_stk_3 + 1
        
        # - contact person -
        row_stk_4 = row_stk_1
        while row_stk_4 < max_rows:
            next_regulation_name = data.iloc[row_stk_4][column_stk_1]

            contact_person = str(data.iloc[row_stk_4][column_stk_1+11])

            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif contact_person == 'nan':
                row_stk_4 = row_stk_4 + 1
            else:
                insert_contact_person = f'''INSERT INTO STAKEHOLDER (STAKEHOLDER_ID, STAKEHOLDER_CLASSIFICATION_ID, STAKEHOLDER_NAME, STAKEHOLDER_POSITION, STAKEHOLDER_NOTES) VALUES ({stk_id}, 3, '{contact_person}', NULL, NULL);'''
                insert_contact_person_2 = f'''INSERT INTO REGULATION_STAKEHOLDER (REG_ID, STAKEHOLDER_ID) VALUES ({reg_id}, {stk_id});'''
                insert_stk_string = insert_stk_string + insert_contact_person + '\n\n'
                insert_reg_stk_string = insert_reg_stk_string + insert_contact_person_2 + '\n\n'
                stk_id = stk_id + 1
                row_stk_4 = row_stk_4 + 1

        reg_id = reg_id + 1
    
    row_stk_1 = row_stk_1 + 1

with open('insertStatementsComplete.sql', 'a') as file:
    file.write('\n\n-- STAKEHOLDER table --\n\n')
    file.write(insert_stk_string)
    file.write('\n\n-- REGULATION_STAKEHOLDER table --\n\n')
    file.write(insert_reg_stk_string)

# --- REVISION table ---

reg_id = 1
insert_rev_string = ''
revision_id = 1
row_rev_1 = 1 # starting from 1st regulation
column_rev_1 = 1
while row_rev_1 < max_rows:
    regulation_name = data.iloc[row_rev_1][column_rev_1]
    
    if str(regulation_name) != 'nan':
        row_rev_2 = row_rev_1
        column_rev_2 = 25

        while row_rev_2 < max_rows:
            revision_value = data.iloc[row_rev_2][column_rev_2]

            next_regulation_name = data.iloc[row_rev_2][column_rev_1]
            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif str(revision_value) == 'nan':
                row_rev_2 = row_rev_2 + 1
                continue
            else:
                rev_editorial_date_xl = data.iloc[row_rev_1][column_rev_1+12]
                if str(rev_editorial_date_xl) != 'nan':
                    rev_editorial_date = rev_editorial_date_xl.strftime('%Y-%m-%d')
                    rev_editorial_date = f"'{rev_editorial_date}'"
                else: 
                    rev_editorial_date = 'NULL'
                
                editorial_change_yn = 1 if str(data.iloc[row_rev_1][column_rev_1+2]) != 'nan' else 0
                rev_editorial_desc = f'''"{str(data.iloc[row_rev_1][column_rev_1+13])}"''' if str(data.iloc[row_rev_1][column_rev_1+13]) != 'nan' else 'NULL'
                insert_revision = f'''INSERT INTO REVISION (REVISION_ID, REG_ID, REVISION_NUMBER, REVISION_DATE, REVISION_EFFECTIVE_DATE, REVISION_DESC, EDITORIAL_CHANGE_YN, REV_EDITORIAL_DATE, REV_EDITORIAL_DESC, DOCUMENTATION_OF_OTHER_REVISION_LINK) VALUES ({revision_id}, {reg_id}, NULL, NULL, NULL, NULL, {editorial_change_yn}, {rev_editorial_date}, {rev_editorial_desc}, NULL);'''
                insert_rev_string = insert_rev_string + insert_revision + '\n\n'

                row_rev_2 = row_rev_2 + 1
                revision_id = revision_id + 1
            
        reg_id = reg_id + 1
    
    row_rev_1 = row_rev_1 + 1

with open('insertStatementsComplete.sql', 'a') as file:
    file.write('\n\n-- REVISION table --\n\n')
    file.write(insert_rev_string)

# -- REVISION_PROCESS table --

reg_id = 1
insert_rev_pro_string = ''
revision_id = 1
revision_pro_id = 1
row_rev_pro_1 = 1 # starting from 1st regulation
column_rev_pro_1 = 1
while row_rev_pro_1 < max_rows:
    regulation_name = data.iloc[row_rev_pro_1][column_rev_pro_1]
    
    if str(regulation_name) != 'nan':
        row_rev_pro_2 = row_rev_pro_1
        column_rev_pro_2 = 25

        while row_rev_pro_2 < max_rows:
            revision_value = data.iloc[row_rev_pro_2][column_rev_pro_2]
            
            next_regulation_name = data.iloc[row_rev_pro_2][column_rev_pro_1]
            if str(next_regulation_name) != 'nan' and str(next_regulation_name) != str(regulation_name):
                break
            elif str(revision_value) == 'nan':
                row_rev_pro_2 = row_rev_pro_2 + 1
                continue
            else:
                bot_approval_date_xl = data.iloc[row_rev_pro_1][column_rev_pro_1+14]
                bot_approval_status = ''
                if str(bot_approval_date_xl) != 'nan':
                    bot_approval_date = bot_approval_date_xl.strftime('%Y-%m-%d')
                    bot_approval_date = f"'{bot_approval_date}'"
                    bot_approval_status = 'Yes'
                else: 
                    bot_approval_date = 'NULL'
                    bot_approval_status = 'No'

                # asec_approval_date logic

                # ipc_approval_date logic
                
                insert_revision_process = f'''INSERT INTO REVISION_PROCESS (REVISION_PROCESS_ID,
                              REVISION_ID,
                              BOT_APPROVAL_DATE,
                              BOT_APPROVAL_STATUS,
                              BOT_PREVIOUS_APPROVAL_DATE,
                              ASEC_APPROVAL_DATE,
                              ASEC_APPROVAL_STATUS,
                              ASEC_PREVIOUS_REVISION_DATE,
                              ASEC_PREVIOUS_REVISION_REVIEW_DATE,
                              IPC_APPROVAL_DATE,
                              IPC_APPROVAL_STATUS,
                              IPC_PREVIOUS_REVISION_DATE,
                              IPC_PREVIOUS_REVISION_REVIEW_DATE,
                              REVISION_PROCESS_NOTES) VALUES 
                              ({revision_pro_id}, {revision_id}, {bot_approval_date}, '{bot_approval_status}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);'''
                insert_rev_pro_string = insert_rev_pro_string + insert_revision_process + '\n\n'

                row_rev_pro_2 = row_rev_pro_2 + 1
                revision_id = revision_id + 1
                revision_pro_id = revision_pro_id + 1

        reg_id = reg_id + 1
    
    row_rev_pro_1 = row_rev_pro_1 + 1

with open('insertStatementsComplete.sql', 'a') as file:
    file.write('\n\n-- REVISION_PROCESS table --\n\n')
    file.write(insert_rev_pro_string)