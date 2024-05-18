fake_users_db = {
    "sayed": {
        "id": 1,
        "username": "sayed",
        "full_name": "Ahmed Abd Elgawad",
        "email": "sayed@example.com",
        # password="g=z%UY334FzY"
        "hashed_password": "$2b$12$xIJZShyOKuTSBdIPPyZpkOr8vJmK0laSucSsFcY1yjixw5u3pnngu",
        "role": "admin",
        "disabled": False,
    },
    "reda": {
        "id": 2,
        "username": "reda",
        "full_name": "Reda Elmesery",
        "email": "reda@example.com",
        # password="KA5=u33|@]8t"
        "hashed_password": "$2b$12$EKeRgu1rSAeOczp1dLAebOSbReMcTR1P0qTYVCiU5M.FgUAI1d3Ay",
        "role": "customer",
        "disabled": False,
    },
    "ibrahim": {
        "id": 3,
        "username": "ibrahim",
        "full_name": "Ibrahim Nour",
        "email": "ibrahim@example.com",
        # password=",@3#62S&#'tp"
        "hashed_password": "$2b$12$xMiVL2TMo0vLmPdV3ltde.9KTVecVE5R9EnIGK5V6CroyQ/CEBazK",
        "role": "customer",
        "disabled": False,
    },
}


fake_order_db = [
    {
        "customer_id": "2",
        "customer": {
            "username": "reda",
            "full_name": "Reda Elmesery",
        },
    },
    {
        "customer_id": "3",
        "customer": {
            "username": "ibrahim",
            "full_name": "Ibrahim Nour",
        },
    },
]
