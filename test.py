import instainfo


userObj = instainfo.UserProfile('grejojoby')
    # Prints the users profile picture URL
print(userObj.GetProfilePicURL())
print(userObj.FollowersCount())
print(userObj.FollowedByCount())
print(userObj.IsPrivate())
print(userObj.IsBusinessAccount())