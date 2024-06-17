feed = input("Enter the feed option (1-Four you / 2-Following): ")
x = "hola"

match feed.upper():
    case 'FOUR YOU' | '1':
        x = "For you"

    case 'FOLLOWING' | '2':
        x = "Following"


print(x)
