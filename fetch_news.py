from newsapi import NewsApiClient
import pycountry
import spacy

# Initialize the News API client
newsapi = NewsApiClient(api_key='9b270ef9964946f882575cb676b91082')



# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

# List of specific sources to choose from
specific_sources = {
    'wsj': 'Wall Street Journal',
    'nyt': 'New York Times',
    'bbc-news': 'BBC News',
    'cnn': 'CNN',
    'abc-news': 'ABC News'
}

while True:
    # Ask the user if they want news from a specific country
    region_choice = input("Do you want news from a specific country? [yes/no]: ").strip().lower()

    if region_choice == 'yes':
        # Take the name of the country from user input
        input_country = input("Country: ")

        # Handle different aliases for the United States
        if input_country.lower() in ['america', 'usa', 'united states of america']:
            input_country = 'United States'
        input_countries = [f'{input_country.strip()}']
        countries = {}

        # Iterate over all countries using pycountry
        for country in pycountry.countries:
            # Store the unique code of each country in the dictionary along with its full name
            countries[country.name] = country.alpha_2

        # Check if the entered country name is valid or invalid using the unique code
        codes = [countries.get(country.title(), 'Unknown code') for country in input_countries]
        country_code = codes[0].lower()
    else:
        country_code = None

    # Ask if the user wants to choose a category or just focus on sources
    category_choice = input("Do you want to choose a category? [yes/no]: ").strip().lower()

    if category_choice == 'yes':
        # Display all categories from which the user will choose
        category = input("Which category are you interested in?\n1.Business\n2.Entertainment\n3.General\n4.Health\n5.Science\n6.Technology\n\nEnter here: ").strip().lower()
    else:
        category = None

    # Display specific sources for user to choose from
    print("\nAvailable specific sources:")
    for key, value in specific_sources.items():
        print(f"{key}: {value}")

    # Ask the user to choose sources
    source_choices = input("\nEnter the keys of the sources you want to include, separated by commas (leave empty for none): ").strip().lower()
    chosen_sources = [key.strip() for key in source_choices.split(',') if key.strip() in specific_sources]

    # Ask the user to input a keyword
    keyword = input("\nEnter a keyword to search for in the headlines (leave empty for none): ").strip().lower()

    if chosen_sources:
        # Fetch the news from the chosen sources
        top_headlines = newsapi.get_top_headlines(
            language='en', sources=','.join(chosen_sources), page_size=20
        )
    elif category and country_code:
        # Fetch the news according to the user's choice of category and region
        top_headlines = newsapi.get_top_headlines(
            category=category, language='en', country=country_code, page_size=20
        )
    elif category:
        # Fetch the news according to the user's choice of category without a specific region
        top_headlines = newsapi.get_top_headlines(
            category=category, language='en', page_size=20
        )
    elif country_code:
        # Fetch the top news from a specific country without any category or source
        top_headlines = newsapi.get_top_headlines(
            language='en', country=country_code, page_size=20
        )
    else:
        # Fetch the top news globally without any category or source
        top_headlines = newsapi.get_top_headlines(
            language='en', page_size=20
        )

    # Fetch the top news under that category
    Headlines = top_headlines['articles']

    # Display the news with good readability for the user
    filtered_articles = []
    if Headlines:
        num = 1
        for i, article in enumerate(Headlines):
            title = article['title'].lower() if article['title'] else ''
            description = article.get('description', '').lower() if article.get('description') else ''
            if keyword in title or keyword in description:
                filtered_articles.append(article)
                print(f"{num}. {article['title']}.")
                if article['description']:
                    doc = nlp(article['description'])
                    summary = ' '.join([sent.text for sent in doc.sents][:2])  # Simplified summarization
                    print(f"Summary: {summary}\n")
                else:
                    print("Summary: No description available to summarize.\n")
                num += 1

        if not filtered_articles:
            print(f"No articles found with the keyword '{keyword}'.")
            print("Try again with a different keyword or without the word altogether.")

    else:
        print("Sorry, no articles found for the selected sources.")

    option = input("\nDo you want to search again [Yes/No]? ")
    if option.lower() != 'yes':
        break
