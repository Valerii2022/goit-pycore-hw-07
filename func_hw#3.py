from datetime import datetime, timedelta

users = [
    {"name": "John Doe", "birthday": "1985.05.08"},
    {"name": "Jane Smith", "birthday": "1990.05.07"},
    {"name": "James Roney", "birthday": "1985.05.09"},
    {"name": "David James", "birthday": "1990.04.22"},
    {"name": "Jo Cole", "birthday": "1988.08.10"},
    {"name": "Steave Smith", "birthday": "1990.05.04"},
    {"name": "Leo Jordan", "birthday": "1993.04.30"},
    {"name": "Denis Roney", "birthday": "1977.04.09"},
    {"name": "Kathy Roney", "birthday": "1980.05.15"},
    {"name": "Austin Jordan", "birthday": "1998.05.05"},
    {"name": "Pall Jobs", "birthday": "1973.05.03"},
    {"name": "Dasty Goover", "birthday": "1985.05.10"},
    {"name": "Kelly Smith", "birthday": "1997.05.12"}
]



def get_upcoming_birthdays(users):
    current_date = datetime.today().date()
    current_timedelta = current_date + timedelta(7)
    current_year = datetime.now().year
    result = []
    for user in users:
        congratulation_date = datetime.strptime(user["birthday"], '%Y.%m.%d').replace(year=current_year).date()
        birthday_this_year = (congratulation_date - current_date).days
        if birthday_this_year < 0:
            congratulation_date = congratulation_date.replace(year=2025)
        if congratulation_date >= current_date and congratulation_date <= current_timedelta:
            if congratulation_date.weekday() == 5:
                congratulation_date = congratulation_date + timedelta(2)
            if congratulation_date.weekday() == 6:
                congratulation_date = congratulation_date + timedelta(1)
            result.append({"name":user["name"], "congratulation_date": f"{congratulation_date}"})
    result.sort(key=lambda x: x["congratulation_date"])
    return result


upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)