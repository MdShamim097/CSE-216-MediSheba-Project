import cx_Oracle

try:
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

except Exception as e:
    print("Fuck this shit ", e)
else:
    try:
        c = conn.cursor()
        data = [2, 1]
        # cursor.callproc('myproc', [123, outVal])
        # result = c.callfunc('update_a_pos_blood', str, data)
        c.callproc('update_cabin_count_in_hospital', data)


    except Exception as e:
        print("Fuck 2", e)

    else:
        print("Done")

    finally:
        c.close()
finally:
    conn.close()

'''

import cx_Oracle

try:
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

except Exception as e:
    print("Fuck this shit ", e)
else:
    try:
        type_obj = conn.gettype('PKG_DEMO.UDT_DEMORECORD')
        obj = type_obj.newobject()
        objee = []
        c = conn.cursor()
        id = [22]
        result = c.callfunc('get_doctor_details', obj, id)

    except Exception as e:
        print("Fuck 2", e)

    else:
        print("Doc name: ", result)


'''
