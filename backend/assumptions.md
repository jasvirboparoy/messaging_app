# Assumptions for Python_powers Group

## Major Assumptions
1. A new token is generated for every session e.g. everytime a user logs in, a new token is generated (active token). When they logout, this token is invalidated. When they log in again, a new token is generated for them.

2. When a user registers, they are automatically logged in to system and hence a session token is generated.

3. The user id is unique to the user and is stored in the system. This id never changes.

## Auth Function Assumptions

### auth_login 
1. Assume that an email is a string seperated into two parts by the @ symbol. The first part is "personal_info" and the second part is the domain. (e.g personal_info@domain)

2. Assume that email isn't case sensitive and will login if case doesn't match system.

4. Assume leading and trailing spaces for passwords will remain hence not allowing login even if valid password typed in with accidental leading or trailing spaces.

### auth_register
1. Assume that leading and trailing spaces won't be removed if accidently entered in email when registering.

### auth_logout
1. Assume that to logout, a user must be logged in to system

## Channel Function Assumptions

### channel_join
1. Assume that when creating a channel whether private or public, it cannot have the same name as another channel public or private - throw an InputError for this case

2. Assume that leading and trailing spaces cannot be entered into channel names

3. Assume that when a channel is created, the user is automatically joined

### channel_messages
1. Assume that messages are ordered by time in list 

### channel_details
1. Assume that the all_members and owner_members lists may not have any order to them

### user_profile

1. Assume that auth_register and user_profile_sethandle works
2. Assume token is always vaild

### user_profile_setname
1. Assume that auth_register works
2. Assume token is always vaild

### user_profile_setemail
1. Assume that auth_register and user_profile_sethandle works
2. Assume token is always vaild

### user_profile_sethandle
1. Assume that auth_register works
2. Assume token is always vaild

### users_all
1. Assume that auth_register and user_profile works
2. Assume token is always vaild

## Message Function Assumptions

### message_send
1. Assume that announcements can be sent to all channels regardless of publicity status

### message_remove
1. Assume members can remove their own message
2. Assume owners and admins can remove other members' message
3. Assume owners and admins cannot remove someone's message if the authorised member has similar or higher privilege

### message_edit
1. Assume members can edit their own message
2. Assume owners and admins can edit other members' message
3. Assume owners and admins cannot edit someone's message if the authorised member has similar or higher privilege

## Search Assumptions

### search
1. Assume the result is returned from all public messages