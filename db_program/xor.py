import random
r = ''
mylist = []
for y in range(5):
    for x in range(8):
        r = r + str(random.randrange(0, 9))
    mylist.append(r)
    r = ''

print(mylist)
cmd_str = """
            insert into employee (name, account_number, password, job, entry_date) values 
            ('Boss Boss', {},'10000001','000000', 'Boss', current_date()),
            ('Shaonan Hu', {},'10000002','111111', 'Engineer', current_date()),
            ('Jiahao Chen', {},'222222', 'Engineer', current_date()),
            ('Jiawei Yang', {},'333333', 'Engineer', current_date()),
            ('Yilun Peng', {},'555555', 'Engineer', current_date())
    """

cmd_str = cmd_str.format(mylist[0], mylist[1], mylist[2], mylist[3], mylist[4])
print(cmd_str)