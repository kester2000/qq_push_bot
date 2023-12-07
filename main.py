from user_loop import UserList

with open('user_list.txt') as f:
    user_list = list(map(int, f.read().split()))

user_list = UserList(user_list)
user_list.run_loop()