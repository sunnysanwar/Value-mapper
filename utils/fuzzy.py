from fuzzywuzzy import fuzz

# Function to find matching suggestions
def find_matching_keywords(user_keyword, keyword_list):
    matching_suggestions = {}
    for keyword in keyword_list:
        similarity_score = fuzz.partial_ratio(user_keyword, keyword)
        if similarity_score >= 80:
            matching_suggestions.update({keyword: similarity_score})
    matching_suggestions = sorted(matching_suggestions.items(), key=lambda x: x[1], reverse=True)
    matching_suggestions = [keyword for keyword, _ in matching_suggestions]
    return matching_suggestions