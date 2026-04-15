
# #! Divisor cannot be zero
# def divide (dividend, divisor):
#     if divisor == 0:
#         raise ZeroDivisionError("Divisor cannot be zero")
    
#     return dividend/divisor

# # result = divide(10, 0)

# # print(result)

# grades = [] 

# try:
#     average = divide(sum(grades), len(grades))
# except ZeroDivisionError as e:
#     print("Cannot calculate the average grade because there are no grades in the list.")
#     print("Error message:", e)
# else:
#     print("The average grade is ", average)
# finally:
#     print("end of calculation")
    
# students = [
#     {"name": "Bob", "grades": [80, 85]},
#     {"name": "Rolf", "grades": []},
#     {"name": "Jen", "grades": [90, 95]}
# ]

# for student in students:
#     try:
#         average = divide(sum(student["grades"]), len(student["grades"]))
#         print(student["name"], "average:", average)
#     except ZeroDivisionError as e:
#         print("Error:", student["name"], "has no grades.")
#         print("Error message:", e)
#     else:
#         print("the average grade for", student["name"], "is", average)
#     finally:
#         print("Finished processing", student["name"])

# users = ["Alice", "Bob", "Charlie"]

# def get_user(index):
#     return users[index]


# user_index = input("Enter user index: ")

# try:
#     user = get_user(int(user_index))
#     print("Selected user:", user)
    
# except IndexError as e:
#     print("user index is out of range.")

# except ValueError as e:
#     print("Invalid input. Please enter a number.")

# else:
#     print("User is exists.")

users = {
    "alice": "1234",
    "bob": "abcd",
    "charlie": "pass"
}

def login(username, password):
   

    if users[username] == password:
        return True 
    return False
username = input("Enter username: ")


try:
    
    if username not in users:
        raise KeyError
    password = input("Enter password: ")  
      
    if  login(username, password):
        print("Login successful")
    else:
        print("Invalid credentials")

        
except KeyError as e:
    print("Error: Username does not exist.")
