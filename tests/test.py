table_data ={'id':'1','name':'xiaomi'}

table_name = 'event'
for i in table_data:
    table_data[i] = "'"+ str(table_data[i])+"'"
print(table_data)
for key in table_data:
    table_data[key] = "'" + str(table_data[key] + "'")

key = ",".join(table_data.keys())
print(key)
value = ','.join(table_data.values())
print(value)
real_sql = "insert into\t" + table_name + "("+key+")VALUES("+value+")"
print(real_sql)
