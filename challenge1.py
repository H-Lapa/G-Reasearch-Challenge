# from 74.34% -> 77.64%
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

    # Dynamic aggression threshold and amplifier based on auction progress and remaining items
    aggression_threshold = 0.55 - 0.05 * auction_progress
    aggression_amplifier = 10 * remaining_items / total_items

    # Apply a sigmoid function to the auction progress to compute a factor that increases smoothly from 0 to 1.
    aggression_factor = sigmoid((auction_progress - aggression_threshold) * aggression_amplifier)

    # Keep track of total item value
    if 'total_item_value' not in player_information:
        player_information['total_item_value'] = 0
    player_information['total_item_value'] += current_victory_points

    average_item_value = player_information['total_item_value'] / (total_items - remaining_items + 1)
    value_ratio = current_victory_points / average_item_value

    # If the last auction was won by someone else and the current item value is higher than average, increase the aggression factor.
    if last_auction_result['winner'] != "player" and last_auction_result['winning_bid'] is not None and last_auction_result['winning_bid'] > remaining_budget / remaining_items and value_ratio > 1:
        aggression_factor += 0.05 * (1 + (last_auction_result['winning_bid'] - remaining_budget / remaining_items))

    # Compute our bid value taking into account the proportional bid value and our aggression factor.
    base_bid_value = remaining_budget * (prop_bid_value + 2 * aggression_factor)

    # Adjust safety buffer based on game progress
    buffer = remaining_budget * 0.1 * (remaining_items / total_items)

    # Consider the average bid in the current bid value
    if last_auction_result['total'] is not None:
        average_bid = last_auction_result['total'] / (game_info['Number_Robots'] + 1)
        if 'average_bids' not in player_information:
            player_information['average_bids'] = []
        player_information['average_bids'].append(average_bid)
    
    if 'average_bids' in player_information and player_information['average_bids']:
        avg_bid = sum(player_information['average_bids']) / len(player_information['average_bids'])
        bid_value = min(base_bid_value + avg_bid, remaining_budget - buffer)
    else:
        bid_value = base_bid_value

    # Adjust bid value based on how much we value the item
    bid_value *= value_ratio

    # Ensure we do not bid over our budget.
    bid_value = min(bid_value, remaining_budget)

    return bid_value

    
## getting data from the system

    # import math

    # Data collection dictionary
    # data = {'bidding_data': []}

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

    #     # Apply a sigmoid function to the auction progress to compute a factor that increases smoothly from 0 to 1.
    #     aggression_factor = sigmoid((auction_progress - 0.55) * 10)

    #     # If the last auction was won by someone else, increase the aggression factor.
    #     if last_auction_result['winner'] != "player" and last_auction_result['winning_bid'] is not None and last_auction_result['winning_bid'] > remaining_budget / remaining_items:
    #         aggression_factor += 0.05 * (1 + (last_auction_result['winning_bid'] - remaining_budget / remaining_items))

    #     # Compute our bid value taking into account the proportional bid value and our aggression factor.
    #     base_bid_value = remaining_budget * (prop_bid_value + 2 * aggression_factor)

    #     # Adjust safety buffer based on game progress
    #     buffer = remaining_budget * 0.1 * (remaining_items / total_items)

    #     # Consider the average bid in the current bid value
    #     if last_auction_result['total'] is not None:
    #         average_bid = last_auction_result['total'] / (game_info['Number_Robots'] + 1)
    #         if 'average_bids' not in player_information:
    #             player_information['average_bids'] = []
    #         player_information['average_bids'].append(average_bid)
        
    #     if 'average_bids' in player_information and player_information['average_bids']:
    #         avg_bid = sum(player_information['average_bids']) / len(player_information['average_bids'])
    #         bid_value = min(base_bid_value + avg_bid, remaining_budget - buffer)
    #     else:
    #         bid_value = base_bid_value

    #     # Keep track of total item value
    #     if 'total_item_value' not in player_information:
    #         player_information['total_item_value'] = 0
    #     player_information['total_item_value'] += current_victory_points

    #     # Adjust bid value based on how much we value the item
    #     average_item_value = player_information['total_item_value'] / (total_items - remaining_items + 1)
    #     value_ratio = current_victory_points / average_item_value
    #     bid_value *= value_ratio

    #     # Ensure we do not bid over our budget.
    #     bid_value = min(bid_value, remaining_budget)

    #     # Add current bid information to data dictionary
    #     data['bidding_data'].append({
    #         'Remaining Budget': remaining_budget,
    #         'Bid Value': bid_value,
    #         'Victory Points of the Item': current_victory_points,
    #         'Remaining Items': remaining_items,
    #         'Auction Progress': auction_progress,
    #         'Aggression Factor': aggression_factor
    #     })
        
    #     # If this is the last auction, raise an exception with the collected data
    #     if remaining_items == 1:
    #         raise Exception(f'Bidding data: {data["bidding_data"]}')

    #     return bid_value
