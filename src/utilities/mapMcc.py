
def map_mcc_to_category(mcc) -> str:
    if mcc in ["5411", "5412"]:
        return "FOOD"
    elif mcc in ["5811", "5812"]:
        return "MEAL"
    else:
        return "CASH"
