from djangomongo.data.supplier import get_user_statistics

res = get_user_statistics()
for i in res:
    print(i)
