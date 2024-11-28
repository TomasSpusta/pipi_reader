import web_requests_class


def main():

    token = web_requests_class.Token("-", "-")
    instrument_mac_address = "e4:5f:01:ea:99:17"
    card_id = 1834257108
    api_key = "ude9c6nezyr71i9vf3jdtye18vwdk81s"  # s"
    token_path = "token_data.txt"

    user = web_requests_class.ApiRequests.fetch_user_data(card_id)
    print("User: " + user.name)

    instrument = web_requests_class.ApiRequests.fetch_instrument_data(
        instrument_mac_address)
    print("Instrument: " + instrument.name)

    is_token_valid = web_requests_class.ApiRequests.validate_token(
        token, token_path, api_key)

    if is_token_valid is True:
        web_requests_class.ApiRequests.start_recording(user, instrument, token)

    '''
    instrument_info = web_requests_class.ApiRequests.fetch_instrument_data(
        instrument_mac_address)
    user_data = web_requests_class.ApiRequests.fetch_user_data(card_id)
    if instrument_info != None:
        print(instrument_info.name + " " + instrument_info.id)
    else:
        print("Box is not in database or box is not assigned to the instrument")
    print(user_data.name + " " + user_data.id)
   
   
    token_base = web_requests_class.Token("-", "-")
    print(token_base.expiration + " " + token_base.string)

    token = web_requests_class.ApiRequests.load_token(
        token_base, token_path)

    is_token_valid = web_requests_class.ApiRequests.check_expiration(token)
    if is_token_valid is True:
        print("Token je OK")

    else:
        token = web_requests_class.ApiRequests.fetch_token(api_key)
        if token != None:
            print("Saving token")
            web_requests_class.ApiRequests.save_token(token)
            print("reseting token")
            token = web_requests_class.Token("-", "-")
            print(token.expiration + " " + token.string)
            print("loading token")

        else:
            print("Problem with get token method, check API")

    #print("Api token")
    #print(token.expiration + " " + token.string)

    # web_requests_class.ApiRequests.get_token(api_key)
    '''


if __name__ == "__main__":
    main()
