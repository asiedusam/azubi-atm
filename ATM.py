# import the json library so we can pull data fron the json file with the user and account details
import hashlib
import json


# function to update the json file with new account details after withdrawals
def update_account():
    with open("accounts.json", "w") as newacc:
        json.dump(users, newacc)


# print the balance of the current user
def print_balance():
    print("Your new balance is \nGHS: {}\nUSD: {}\n\n".format(
        user["balance"]["GHS"],
        user["balance"]["USD"])
    )


def currency_error():
    print(valerr + "\n1 for GHS\n2 for USD\n")


# check if the user has enough balance and make a withdrawal
def withdraw_money():
    while True:
        currency = input(
            "Which account do you want to withdraw from?\n1: GHS\n2: USD\n")
        try:
            if int(currency) == 1:
                denomination = "GHS"
            elif int(currency) == 2:
                denomination = "USD"
            else:
                currency_error()
                continue
            try:
                amount = float(input("How much do you want to withdraw?\n"))
            except ValueError:
                print("Please type a number")
        except ValueError:
            print(valerr + "\n1 for GHS\n2 for USD\n")
        try:
            if float(amount) <= user["balance"][denomination]:
                user["balance"][denomination] = round((user["balance"][denomination] - amount), 2)
                print_balance()
                update_account()
                break
            else:
                print(sorry)
        except ValueError:
            print(valerr)


# function to hash pin
def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


# function for the user to transfer money to a different account
def transfer_money():
    while True:
        # prompt the user to enter the destination account username
        to_account = input("Type the username of the account you want to transfer money to.\n")
        for to_user in users:
            # confirm if the account exists
            if to_account in to_user["username"]:
                while True:
                    # prompt user to select which account to transfer from
                    currency = input(
                        "Which account do you want to transfer from?\n1: GHS\n2: USD\n")
                    try:
                        if int(currency) == 1:
                            denomination = "GHS"
                        elif int(currency) == 2:
                            denomination = "USD"
                        else:
                            currency_error()
                            continue
                        try:
                            # prompt the user to enter the amount to be transferred.
                            amount = float(input("How much do you want to transfer?\n"))
                        except ValueError:
                            print("Please type a number")
                    except ValueError:
                        print(valerr + "\n1 for GHS\n2 for USD\n")
                    try:
                        # if amount entered is not more than the user's balance,
                        # make the transfer and show the balance
                        if float(amount) <= user["balance"][denomination]:
                            user["balance"][denomination] = round((user["balance"][denomination] - amount), 2)
                            to_user["balance"][denomination] = round((to_user["balance"][denomination] + amount), 2)
                            update_account()
                            print("{} {} has been successfully transferred to {}".format(
                                amount, denomination, to_account.capitalize()))
                            print_balance()
                            break
                        else:
                            print(sorry)
                    except ValueError:
                        print(valerr)


# function for the user to change pin
def change_pin():
    old_pin = hash_password(input("Please type your old pin: \n"))
    try:
        if old_pin == user["pin"]:
            while True:
                n_pin = input("Please type your new pin: \n")
                if len(n_pin) == 4 and n_pin.isdecimal() is True \
                        and hash_password(n_pin) != old_pin:
                    new_pin = hash_password(n_pin)
                    user["pin"] = new_pin
                    update_account()
                    print("Your pin has been successfully changed. \n"
                          "Please log in again to continue.\n")
                    break

                else:
                    print("Sorry, your pin has not been changed.\n"
                          "Please check your new pin.\n")
                    continue

    except ValueError:
        print(valerr)


# start the program
if __name__ == '__main__':
    # open the json file
    with open("accounts.json", "r") as accountsfile:
        users = json.load(accountsfile)
        valerr = "Please type a number \n"
        sorry = "Sorry, you do not have enough money in this account\n\n"
        print("\nWelcome to MY ATM")
        # keep the program running until an arbitrary break is called
        while True:
            username = input("\n\nPlease type your username to log in: \n").lower()
            # loop through users to see if the name given by the user exists
            for user in users:
                if username in user["username"] and user["active"] is True:
                    tries = 0
                    while True:
                        # prompt the user to enter a pin and hash it to confirm or deny access
                        pin = hash_password(input("Please type your pin: \n"))
                        # if the hashed pin matches the one in the data file, grant access
                        if pin == user["pin"]:
                            print("You have successfully logged in")
                            while True:
                                # prompt user to perform one of four actions
                                action = input("1: Check Balance "
                                               "\n2: Withdraw Money \n3: Transfer Money\n"
                                               "4: Change Pin \n5: Exit\nEnter Option Here: \n")
                                try:
                                    # call a function based on the user's input
                                    if int(action) == 1:
                                        # this is a function to print the user's account balance
                                        print_balance()
                                    elif int(action) == 2:
                                        # this is a function for te user to make a withdrawal
                                        withdraw_money()

                                    elif int(action) == 3:
                                        # this is a function for te user to transfer money to another account
                                        transfer_money()
                                        break
                                    elif int(action) == 4:
                                        change_pin()
                                        break
                                    elif int(action) == 5:
                                        # exit
                                        break
                                except ValueError:
                                    # if the user does not type a number, prompt to retry
                                    print(valerr)
                            break
                        else:
                            # if the user enters a wrong pin, update the number of tries by 1.
                            # After 3 unsuccessful tries, deactivate that account.
                            tries += 1

                            if tries == 3:
                                user["active"] = False
                                print("Your card has been deactivated.\n"
                                      "Please contact the nearest branch to reactivate.")
                                update_account()
                                break
                            print(
                                "Sorry, wrong pin :(\nPlease retry. \n"
                                "Entering the wrong pin 3 times will lead to your card being deactivated!\n"
                                "Unsuccessful Attempts: {}\n"
                                    .format(tries))
                elif username in user["username"] and user["active"] is False:
                    print("Sorry, your card is inactive. Please contact the nearest branch. \n")
