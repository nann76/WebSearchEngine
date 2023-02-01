import UserUnit

uu=UserUnit.UserUnit()

usr_pd={}
usr_pd['1']="1"

usr_hs={}
hs=[]
hs.extend(['sadd ads asd ad '])
hs.extend(['sadd ads asdasdfasdfsdf '])
usr_hs['1']=hs

print(usr_hs)
print(usr_pd)

# uu.usr_hs=usr_hs
# uu.usr_pd=usr_pd
uu.save(usr_pd,usr_hs)

uu.load()
print(uu.usr_pd,usr_hs)

