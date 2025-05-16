def calculate_ltv_gain(answer_rate_increase, customer_segment_size=50000, uplift_rate=0.085, ltv_per_customer=2000, years=3):
    """Annualized LTV gain calculation."""
    additional_retained = customer_segment_size * (answer_rate_increase / 100) * uplift_rate
    total_ltv = additional_retained * ltv_per_customer
    return total_ltv / years
