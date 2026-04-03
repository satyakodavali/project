from werkzeug.security import check_password_hash

hash_val = 'scrypt:32768:8:1$ARD8iu2R30ZgOvjn$0c28fb2c347ac069a47026ad5d1f981cf505bbde11b1e3626b8a21147aa73e5d94d807b682b1299e2029c5c2f76884672524bbc1c3de85f345c28f406888dfe1'
pwd = 'Pass123!'

print(f"Check result: {check_password_hash(hash_val, pwd)}")
