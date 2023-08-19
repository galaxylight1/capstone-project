-- Create Views

CREATE VIEW AllPolicies AS
SELECT POL_ID, POL_NUMBER, POL_TITLE, POL_VERSION_NUMBER, POL_STORAGE_LINK, POL_NOTES 
FROM POLICY;

CREATE VIEW AllRegulations AS
SELECT *
FROM REGULATION;

CREATE VIEW PolicyAndRegulations AS
SELECT P.POL_ID, P.POL_NUMBER, P.POL_TITLE, R.REG_ID, R.REG_NUMBER, R.REG_TITLE, R.REG_STATUS
FROM POLICY P 
JOIN REGULATION R ON P.POL_ID = R.POL_ID;

CREATE VIEW RegulationAndCitations AS
SELECT R.REG_ID, R.REG_NUMBER, C.CITATION_NAME, C.CITATION_STORAGE_LINK
FROM REGULATION R 
JOIN REGULATION_CITATION RC ON R.REG_ID = RC.REG_ID
JOIN CITATION C ON RC.CITATION_ID = C.CITATION_ID;

CREATE VIEW RegulationAndStakeholders AS
SELECT R.REG_ID, R.REG_NUMBER, S.STAKEHOLDER_NAME, S.STAKEHOLDER_POSITION
FROM REGULATION R 
JOIN REGULATION_STAKEHOLDER RS ON R.REG_ID = RS.REG_ID
JOIN STAKEHOLDER S ON RS.STAKEHOLDER_ID = S.STAKEHOLDER_ID;

CREATE VIEW RegulationWithReviewDetails AS
SELECT R.REG_ID, R.REG_NUMBER, RV.REVISION_NUMBER, RV.REVISION_DATE, RV.REVISION_EFFECTIVE_DATE, RV.EDITORIAL_CHANGE_YN, RV.REV_EDITORIAL_DESC
FROM REGULATION R 
JOIN REVISION RV ON R.REG_ID = RV.REG_ID;

CREATE VIEW RegulationApprovalStatus AS
SELECT R.REG_ID, R.REG_NUMBER, RP.BOT_APPROVAL_STATUS, RP.ASEC_APPROVAL_STATUS, RP.IPC_APPROVAL_STATUS
FROM REGULATION R 
JOIN REVISION RV ON R.REG_ID = RV.REG_ID
JOIN REVISION_PROCESS RP ON RV.REVISION_ID = RP.REVISION_ID;

CREATE VIEW AllCitations AS
SELECT *
FROM CITATION;

CREATE VIEW RegulationClassification AS
SELECT R.REG_ID, R.REG_NUMBER, RC.REG_CLASSIFICATION_NAME
FROM REGULATION R 
JOIN REGULATION_CLASSIFICATION RC ON R.REG_CLASSIFICATION_ID = RC.REG_CLASSIFICATION_ID;

CREATE VIEW StakeholderClassification AS
SELECT S.STAKEHOLDER_ID, S.STAKEHOLDER_NAME, S.STAKEHOLDER_POSITION, SC.STAKEHOLDER_CLASSIFICATION_NAME
FROM STAKEHOLDER S 
JOIN STAKEHOLDER_CLASSIFICATION SC ON S.STAKEHOLDER_CLASSIFICATION_ID = SC.STAKEHOLDER_CLASSIFICATION_ID;


-- Call Views

-- 1. AllPolicies: Contains all records from the POLICY table.
-- Can be used to get an overview of all policies.
SELECT * FROM AllPolicies;

-- 2. AllRegulations: Contains all records from the REGULATION table.
-- Can be used to get an overview of all regulations.
SELECT * FROM AllRegulations;

-- 3. PolicyAndRegulations: Combines policy information with related regulations.
-- Can be used to get a detailed overview of a policy with all its related regulations.
SELECT * FROM PolicyAndRegulations;

-- 4. RegulationAndCitations: Combines regulation information with related citations.
-- Can be used to get a detailed overview of a regulation with all its related citations.
SELECT * FROM RegulationAndCitations;

-- 5. RegulationAndStakeholders: Combines regulation information with related stakeholders.
-- Can be used to get a detailed overview of a regulation with all its related stakeholders.
SELECT * FROM RegulationAndStakeholders;

-- 6. RegulationWithReviewDetails: Combines regulation information with related review details.
-- Can be used to get a detailed overview of a regulation with all its related review details.
SELECT * FROM RegulationWithReviewDetails;

-- 7. RegulationApprovalStatus: Combines regulation information with related approval status.
-- Can be used to get a detailed overview of a regulation with its approval status.
SELECT * FROM RegulationApprovalStatus;

-- 8. AllCitations: Contains all records from the CITATION table.
-- Can be used to get an overview of all citations.
SELECT * FROM AllCitations;

-- 9. RegulationClassification: Combines regulation information with related classification.
-- Can be used to get a detailed overview of a regulation with its classification.
SELECT * FROM RegulationClassification;

-- 10. StakeholderClassification: Combines stakeholder information with related classification.
-- Can be used to get a detailed overview of a stakeholder with its classification.
SELECT * FROM StakeholderClassification;