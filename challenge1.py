import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def auction_bids(game_info, current_info, last_auction_result, player_information):
    remaining_budget = current_info['remaining_budget']
    remaining_items = current_info['Remaining_Number_Items']
    current_victory_points = current_info['vp']
    total_items = game_info['Total_Number_Items']

    # Compute the proportional bid value based on the victory points.
    prop_bid_value = current_victory_points / remaining_items

    # Compute how far we are into the auction, ranging from 0 to 1.
    auction_progress = 1 - (remaining_items / total_items)

    # We apply a sigmoid function to the auction progress to compute a factor that increases smoothly from 0 to 1.
    # This makes us bid more aggressively towards the end of the auction.
    aggression_factor = sigmoid((auction_progress - 0.55) * 10)

    # Compute our bid value taking into account the proportional bid value and our aggression factor.
    # We multiply the aggression factor by a constant factor to make our bidding strategy more competitive.
    base_bid_value = remaining_budget * (prop_bid_value + 2 * aggression_factor)

    # Create a safety buffer to save a part of our budget for remaining items.
    buffer = remaining_budget * 0.1

    # Update player_information with the average bid if it exists
    if last_auction_result['total'] is not None:
        average_bid = last_auction_result['total'] / (game_info['Number_Robots'] + 1)
        if 'average_bids' not in player_information:
            player_information['average_bids'] = []
        player_information['average_bids'].append(average_bid)
    
    # Consider the average bid in the current bid value
    if 'average_bids' in player_information and player_information['average_bids']:
        avg_bid = sum(player_information['average_bids']) / len(player_information['average_bids'])
        bid_value = min(base_bid_value + avg_bid, remaining_budget - buffer)
    else:
        bid_value = base_bid_value

    # Ensure we do not bid over our budget.
    bid_value = min(bid_value, remaining_budget)

    return bid_value

## getting data from the system

    # import math

    # def sigmoid(x):
    #     return 1 / (1 + math.exp(-x))

    # def auction_bids(game_info, current_info, last_auction_result, player_information):
    #     remaining_budget = current_info['remaining_budget']
    #     remaining_items = current_info['Remaining_Number_Items']
    #     current_victory_points = current_info['vp']
    #     total_items = game_info['Total_Number_Items']

    #     # Compute the proportional bid value based on the victory points.
    #     prop_bid_value = current_victory_points / remaining_items

    #     # Compute how far we are into the auction, ranging from 0 to 1.
    #     auction_progress = 1 - (remaining_items / total_items)

    #     # We apply a sigmoid function to the auction progress to compute a factor that increases smoothly from 0 to 1.
    #     # This makes us bid more aggressively towards the end of the auction.
    #     aggression_factor = sigmoid((auction_progress - 0.55) * 10)

    #     # Compute our bid value taking into account the proportional bid value and our aggression factor.
    #     # We multiply the aggression factor by a constant factor to make our bidding strategy more competitive.
    #     base_bid_value = remaining_budget * (prop_bid_value + 2 * aggression_factor)

    #     # Create a safety buffer to save a part of our budget for remaining items.
    #     buffer = remaining_budget * 0.1

    #     # Update player_information with the average bid if it exists
    #     if last_auction_result['total'] is not None:
    #         average_bid = last_auction_result['total'] / (game_info['Number_Robots'] + 1)
    #         if 'average_bids' not in player_information:
    #             player_information['average_bids'] = []
    #         player_information['average_bids'].append(average_bid)
        
    #     # Consider the average bid in the current bid value
    #     if 'average_bids' in player_information and player_information['average_bids']:
    #         avg_bid = sum(player_information['average_bids']) / len(player_information['average_bids'])
    #         bid_value = min(base_bid_value + avg_bid, remaining_budget - buffer)
    #     else:
    #         bid_value = base_bid_value

    #     # Collect data for analysis
    #     data = {
    #         "Remaining Budget": remaining_budget,
    #         "Bid Value": bid_value,
    #         "Victory Points of the Item": current_victory_points,
    #         "Remaining Items": remaining_items,
    #         "Auction Progress": auction_progress,
    #         "Aggression Factor": aggression_factor
    #     }
    #     if last_auction_result['winner'] is not None:
    #         data["Winner of the Last Auction"] = last_auction_result['winner']
    #         data["Winning Bid of the Last Auction"] = last_auction_result['winning_bid']
    #     if 'average_bids' in player_information and player_information['average_bids']:
    #         data["Average Bid of Past Items"] = avg_bid

    #     if 'bidding_data' not in player_information:
    #         player_information['bidding_data'] = []
    #     player_information['bidding_data'].append(data)

    #     # If it's the last item in the round, raise an exception with the bidding data
    #     if remaining_items == 1:
    #         raise Exception("Bidding data: " + str(player_information['bidding_data']))

    #     # Ensure we do not bid over our budget.
    #     bid_value = min(bid_value, remaining_budget)

    #     return bid_value