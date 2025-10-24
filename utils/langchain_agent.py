import requests

def generate_fallback_response(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url)
        data = response.json()
        if 'AbstractText' in data and data['AbstractText']:
            return data['AbstractText']
        elif 'Answer' in data and data['Answer']:
            return data['Answer']
        elif 'Definition' in data and data['Definition']:
            return data['Definition']
        else:
            return "I'm still learning and improving. Your question helps me grow smarter!"
    except Exception as e:
        print(f"Error in web search: {e}")
        return "I'm still learning and improving. Your question helps me grow smarter!"

def web_search_fallback(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url)
        data = response.json()
        if 'AbstractText' in data and data['AbstractText']:
            return data['AbstractText']
        elif 'Answer' in data and data['Answer']:
            return data['Answer']
        elif 'Definition' in data and data['Definition']:
            return data['Definition']
        else:
            return None
    except Exception as e:
        print(f"Error in web search: {e}")
        return None
