CREATE OR REPLACE FUNCTION get_doctor_details(
  id IN  MEDI_SHEBA.DOCTOR.DOCTOR_ID%TYPE
) RETURN MEDI_SHEBA.DOCTOR%ROWTYPE
AS
  l_cust_record MEDI_SHEBA.DOCTOR%ROWTYPE;
BEGIN
  SELECT *
  INTO   l_cust_record
  FROM   MEDI_SHEBA.DOCTOR
  WHERE  DOCTOR_ID=id;
  RETURN l_cust_record;
END;
/
/*
DECLARE
  r_acct  MEDI_SHEBA.DOCTOR%ROWTYPE;
BEGIN
     r_acct := get_doctor_details(1);
		 DBMS_OUTPUT.PUT_LINE( r_acct.FIRST_NAME ||'  ' ||	r_acct.LAST_NAME || '  ' || r_acct.PHONE || '   '||r_acct.LOCATION || '  ' || r_acct.EMAIL || '  ' || r_acct.HOSPITAL_ID || '  ' || r_acct.FEES || '  ' || r_acct.SPECIALIZATION);
END;
/
*/