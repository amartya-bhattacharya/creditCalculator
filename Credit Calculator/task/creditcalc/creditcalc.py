import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()
argsDict = vars(args)
params = 0
negValues = False
for key, value in argsDict.items():
    if value:
        params += 1
        if value[0] == "-":
            negValues = True

if (args.type == "diff" and args.payment is not None) or params < 4 or negValues or args.interest is None:
    print("Incorrect parameters")
    exit()


def calcDiff(p, i, n, m):
    d = math.ceil(p / n + i * (p - (p * (m - 1)) / n))
    print("Month", currMonth, ": payment is", d)
    return d


def calcAnnuity(i, p=0, n=0, a=0):
    if a == 0:
        a = math.ceil(p * (i * math.pow(i + 1, n)) / (math.pow(i + 1, n) - 1))
        print("Your annuity payment = " + str(a) + "!")
        print("Overpayment =", a * n - p)
    elif p == 0:
        p = math.ceil(a / ((i * math.pow(i + 1, n)) / (math.pow(i + 1, n) - 1)))
        print("Your loan principal =", str(p) + "!")
        print("Overpayment =", a * n - p)
    elif n == 0:
        x = a / (a - i * p)
        n = math.ceil(math.log(x, i + 1))
        y = math.floor(n / 12)
        m = n % 12
        if m == 0:
            print("You need", str(y), "years to repay this credit!")
        else:
            print("You need", str(y), "years and", str(m), "months to repay this credit!")
        print("Overpayment =", n * a - p)


if args.type == "diff":
    principal = int(args.principal)
    numPayments = int(args.periods)
    interest = float(args.interest) / (12 * 100)
    totalPayments = 0
    for currMonth in range(1, numPayments + 1):
        diff = calcDiff(principal, interest, numPayments, currMonth)
        totalPayments += diff
    over = totalPayments - principal
    print("Overpayment =", over)
elif args.type == "annuity":
    interest = float(args.interest) / (12 * 100)
    if args.payment is None:
        args.payment = 0
    elif args.principal is None:
        args.principal = 0
    elif args.periods is None:
        args.periods = 0
    principal = int(args.principal)
    numPayments = int(args.periods)
    monthlyPayment = int(args.payment)
    calcAnnuity(interest, principal, numPayments, monthlyPayment)
