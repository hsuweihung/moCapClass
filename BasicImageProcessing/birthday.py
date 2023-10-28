month = int(input("birthday month:"))
day=int(input("birthday date: "))

if (month == 3  and day >=21) or (month == 4 and day <= 19):
    print('Aries')
elif (month == 4  and day >=20) or (month == 5 and day <= 20):
    print('Taurus')
elif (month == 5  and day >=21) or (month == 6 and day <= 21):
    print('Gemini')
elif (month == 6  and day >=22) or (month == 7 and day <= 22):
    print('Cancer')
elif (month == 7  and day >=23) or (month == 8 and day <= 22):
    print('Leo')
elif (month == 8  and day >=23) or (month == 9 and day <= 22):
    print('Virgo')
elif (month == 9  and day >=23) or (month == 10 and day <= 23):
    print('Libra')
elif (month == 10  and day >=24) or (month == 11 and day <= 21):
    print('Scorpio')
elif (month == 11  and day >=22) or (month == 12 and day <= 20):
    print('Sagittarius')
elif (month == 12  and day >=21) or (month == 1 and day <= 20):
    print('Capricorn')
elif (month == 1  and day >=21) or (month == 2 and day <= 19):
    print('Aquarius')
elif(month == 2  and day >=20) or (month == 3 and day <= 20):
    print('Pisces')
else:
    print('not a correct input')
