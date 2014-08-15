STRONGLY_LOWERED = 0
REDUCED = 1
NEUTRAL = 2
SLIGHTLY_ELEVATED = 3
ELEVATED = 4

TOTAL_BUCKETS = 5

def get_label(id):
    if id == 0:
        return "strongly lowered"
    if id == 1:
        return "reduced"
    if id == 2:
        return "neutral"
    if id == 3:
        return "slightly elevated"
    if id == 4:
        return "elevated"
    return "unknown id"