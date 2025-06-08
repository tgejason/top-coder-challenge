import sys
import decimal # Use decimal for precise floating-point arithmetic if needed

# Set up decimal context for precise rounding
# This is crucial for financial calculations to avoid floating point inaccuracies
# The challenge requires rounding to 2 decimal places.
D = decimal.Decimal
decimal.getcontext().prec = 10 # Set precision high enough for intermediate calculations
# Use ROUND_HALF_UP or ROUND_HALF_EVEN as per challenge rules, if specified, otherwise default
# For now, we'll use a simple round() at the end, but be aware of float issues.


def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Convert inputs to appropriate types
    trip_duration_days = int(trip_duration_days)
    miles_traveled = int(miles_traveled)
    total_receipts_amount = float(total_receipts_amount) # Use float for now, but be careful with precision

    reimbursement = 0.0 # Initialize reimbursement

    # --- Derive common intermediate values ---
    daily_receipt_spending = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else 0
    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0


    # --- Apply Rules based on your analysis insights ---

    # Rule A: .49 / .99 Receipt Ending Penalty (Very strong evidence from your analysis)
    receipt_cents = int(total_receipts_amount * 100) % 100
    if receipt_cents == 49 or receipt_cents == 99:
        # THIS IS A HYPOTHESIS YOU NEED TO CONFIRM FROM PRD/INTERVIEWS/DATA
        # Based on your output, these endings resulted in *significantly lower* output.
        # Example: A fixed penalty deduction? Or a different calculation path?
        # For demonstration, let's assume a significant flat penalty IF receipts are submitted.
        # You need to determine the exact penalty amount or rule.
        # If the rule is that for these endings, a different, lower reimbursement calculation kicks in:
        #   reimbursement = some_lower_calculation_function(...)
        # else:
        #   # continue with normal rules
        pass # Implement the exact penalty/alternative calculation here. This is crucial!

    # Rule B: Daily Spending Limits (Counter-intuitive: Exceeding leads to HIGHER reimbursement)
    # You identified limits: Short (<=3 days, >75), Medium (4-6 days, >120), Long (>6 days, >90)
    # This implies a branching logic:
    if trip_duration_days <= 3: # Short trips
        if daily_receipt_spending > 75:
            # Path for short trips EXCEEDING daily limit
            # This seems to correlate with higher reimbursement.
            # It could be full receipt reimbursement, plus mileage, plus a small per diem.
            reimbursement += total_receipts_amount # Example: Assume full receipts + other factors
            # You need to derive the exact formula for this path.
        else:
            # Path for short trips WITHIN daily limit
            # This seems to correlate with lower reimbursement (e.g., fixed per diem only).
            # Example: fixed per diem for short trips, maybe minimal or no receipt reimbursement.
            reimbursement += (trip_duration_days * 100) # Example: Simple per diem
            # You need to derive the exact formula for this path.
    elif trip_duration_days <= 6: # Medium trips (4-6 days)
        if daily_receipt_spending > 120:
            # Path for medium trips EXCEEDING daily limit
            pass # Derive formula
        else:
            # Path for medium trips WITHIN daily limit
            pass # Derive formula
    else: # Long trips (>6 days)
        if daily_receipt_spending > 90:
            # Path for long trips EXCEEDING daily limit (your "Vacation Penalty" leading to higher output)
            pass # Derive formula
        else:
            # Path for long trips WITHIN daily limit
            pass # Derive formula


    # Rule C: Mileage Reimbursement
    # This is almost certainly a rate per mile. You need to find the rate.
    # It could be a flat rate, or tiered (e.g., first 100 miles at $X, then $Y).
    # Your analysis didn't explicitly pinpoint mileage rates, but it's a key input.
    # Example:
    # reimbursement += miles_traveled * 0.50 # Hypothetical rate


    # Rule D: 5-Day Trip Special Case
    # Your analysis showed 5-day trips behave differently.
    # This might be an adjustment to the per diem or a specific fixed bonus/penalty.
    if trip_duration_days == 5:
        # Apply 5-day specific adjustment/calculation.
        pass # Implement here

    # Rule E: "Sweet Spot Combo" (5-day, 180+ miles/day, <$100 daily spending)
    # Your analysis showed this leads to *lower* output.
    # This might be an override to a fixed, lower reimbursement.
    if trip_duration_days == 5 and miles_per_day >= 180 and daily_receipt_spending < 100:
        # Apply specific lower reimbursement logic
        pass # Implement here


    # ... (Add more rules as you discover them, e.g., edge cases, minimums, maximums)

    # Final Rounding to 2 decimal places
    # Use decimal.Decimal for proper financial rounding
    # For simplicity, using built-in round for now, but be aware of float precision.
    return round(reimbursement, 2)


if __name__ == "__main__":
    # Read command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>", file=sys.stderr)
        sys.exit(1)

    trip_duration_days = sys.argv[1]
    miles_traveled = sys.argv[2]
    total_receipts_amount = sys.argv[3]

    # Calculate and print the reimbursement
    result = calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount)
    print(result)