# Main Pipi reader file
'''
1. Check internet connection, obtain IP and MAC address => internet module
2. Check and obtain equipment_id and equipment_name from CRM via MAC address
3. Wait till card is obtained - card_id
4. Check if user (card_id) is in CRM database, if yes obtain user_id, user_name etc. 
    if use is not in database, show message to visit user office
5. With user_id and equipment_id check reservation
    depending on response from booking system start recording
        - obtain reservation_id an recording_id
    or display error message (400, 404, 500)
6. Every X (5 now) seconds check remaining_time of reservation (and files acquirec)
7. If remaining_time is near end of reservation show message about the end
8. If button is pressed, end recording (send reservation?_id and equipment_id) 

'''

'''
Import section

'''

'''

'''