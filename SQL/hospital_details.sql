CREATE OR REPLACE FUNCTION get_hospital_details(
  id IN  MEDI_SHEBA.HOSPITAL.HOSPITAL_ID%TYPE
) RETURN MEDI_SHEBA.HOSPITAL%ROWTYPE
AS
  l_cust_record MEDI_SHEBA.HOSPITAL%ROWTYPE;
BEGIN
  SELECT *
  INTO   l_cust_record
  FROM   MEDI_SHEBA.HOSPITAL
  WHERE  HOSPITAL_ID=id;

  RETURN l_cust_record;
END;
/
/*
DECLARE
  r_acct  MEDI_SHEBA.HOSPITAL%ROWTYPE;
BEGIN
     r_acct := get_hospital_details(1);
		 DBMS_OUTPUT.PUT_LINE( r_acct.HOSPITAL_NAME ||'  ' ||	r_acct.LOCATION || '  ' || r_acct.CAPACITY|| '  ' || r_acct.FIRST_NAME|| '  ' || r_acct.LAST_NAME);
END;
/
 */