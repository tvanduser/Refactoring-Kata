import math

# ============== Helper functions ==============

# Helper function for calculating the amount for a performance 
def amount_for(aPerformance, play):
    result = 0
    if play['type'] == "tragedy":
        result = 40000
        if aPerformance['audience'] > 30:
            result += 1000 * (aPerformance['audience'] - 30)
    elif play['type'] == "comedy":
        result = 30000
        if aPerformance['audience'] > 20:
            result += 10000 + 500 * (aPerformance['audience'] - 20)

        result += 300 * aPerformance['audience']

    else:
        raise ValueError(f'unknown type: {play["type"]}')
    return result

# Function to get the play for a performance
def play_for(aPerformance, plays):
    return plays[aPerformance['playID']]

# =========== This is what I am refactoring ===========

# Main function to generate the statement 
def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount):
        return f"${amount:0,.2f}"

    # This calculates the cost for each performance
    for perf in invoice['performances']:
        this_amount = amount_for(perf, play_for(perf, plays)) #calling the helper function that I wrote up above

        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)

        # add extra credit for every ten comedy attendees
        if "comedy" == play_for(perf, plays)["type"]:
            volume_credits += math.floor(perf['audience'] / 5)
        # print line for this order
        result += f' {play_for(perf, plays)["name"]}: {format_as_dollars(this_amount/100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount

    result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result


