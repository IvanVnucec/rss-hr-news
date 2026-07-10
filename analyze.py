import json
import re
from collections import Counter, defaultdict
from datetime import datetime

STOPWORDS = {
    'a', 'ako', 'ali', 'bi', 'bih', 'bila', 'bili', 'bilo', 'bio',
    'bismo', 'biste', 'biti', 'bumo', 'da', 'do', 'duž', 'dva', 'dvije',
    'dalje', 'danas', 'dok', 'evo', 'ga', 'gdje', 'gotovo', 'hoće',
    'hoćemo', 'hoćete', 'hoćeš', 'hoću', 'i', 'iako', 'ih', 'ima', 'iz',
    'između', 'ja', 'je', 'jedan', 'jedna', 'jedne', 'jedno', 'jer',
    'jesam', 'jesi', 'jesmo', 'jest', 'jeste', 'jesu', 'jim', 'joj',
    'još', 'ju', 'kad', 'kada', 'kako', 'kao', 'kod', 'koja', 'kojeg',
    'kojem', 'koji', 'kojima', 'kojoj', 'koju', 'koliko', 'kroz', 'li',
    'me', 'među', 'mene', 'meni', 'mi', 'mimo', 'milijuna', 'moj', 'moja',
    'moje', 'može', 'mogu', 'mogao', 'mora', 'mu', 'na', 'nad', 'nakon',
    'nam', 'nama', 'nas', 'najmanje', 'naš', 'naša', 'naše', 'našeg',
    'ne', 'nego', 'neka', 'neki', 'nekog', 'neku', 'nema', 'netko',
    'neće', 'nećemo', 'nećete', 'nećeš', 'neću', 'nešto', 'ni', 'nije',
    'nikoga', 'nikoje', 'nikoju', 'nisam', 'nisi', 'nismo', 'niste',
    'nisu', 'njega', 'njegov', 'njegova', 'njegovo', 'njemu', 'njezin',
    'njezina', 'njezino', 'njih', 'njihov', 'njihova', 'njihovo', 'njim',
    'njima', 'njoj', 'nju', 'no', 'o', 'od', 'odmah', 'oko', 'on', 'ona',
    'oni', 'ono', 'ovaj', 'ova', 'ove', 'ovog', 'ovo', 'pa', 'pak',
    'pet', 'po', 'pod', 'pored', 'ponovno', 'prije', 'sad', 'sada', 's',
    'sa', 'sam', 'samo', 'se', 'sebe', 'sebi', 'si', 'smo', 'ste', 'su',
    'sve', 'svi', 'svih', 'svog', 'svoj', 'svoja', 'svoje', 'svom', 'ta',
    'tada', 'taj', 'tako', 'te', 'tebe', 'tebi', 'ti', 'tijekom', 'to',
    'toj', 'tome', 'treba', 'tri', 'tu', 'tvoj', 'tvoja', 'tvoje', 'u',
    'unatoč', 'uoči', 'uz', 'vam', 'vama', 'vas', 'vaš', 'vaša', 'vaše',
    'već', 'vi', 'više', 'vrlo', 'za', 'zar', 'zbog', 'zašto', 'će',
    'ćemo', 'ćete', 'ćeš', 'ću', 'četiri', 'čak', 'što', 'tko', 'koje',
    'prema', 'bez', 'ili',
}

if __name__ == '__main__':
    try:
        # Open and read the JSONL file containing articles
        with open('articles.jsonl') as f:
            articles = [json.loads(line) for line in f]
    except (json.JSONDecodeError, IOError) as e:
        # Handle errors related to file reading or JSON parsing
        print(f"Error reading or parsing file: {e}")
        exit(1)

    # Group articles by week of the year
    grouped_articles = defaultdict(list)
    for article in articles:
        # Parse the datetime string to get week and year
        article_date = datetime.strptime(article['datetime'], '%Y-%m-%d %H:%M:%S')
        year, week = article_date.isocalendar()[:2]
        week_in_year = f"{year}-W{week:02d}"
        grouped_articles[week_in_year].append(article)

    # Collect all words from titles and descriptions for each week
    all_words_by_week = defaultdict(list)
    for week_in_year, week_articles in grouped_articles.items():
        for article in week_articles:
            # Combine title and description, convert to lowercase, and split into words
            text = (article.get('title') or '') + ' ' + (article.get('description') or '')
            text = text.lower().strip()
            words = [re.sub(r'^\W+|\W+$', '', word) for word in text.split()]
            # Add words to the week's list if they are at least 3 characters long
            all_words_by_week[week_in_year].extend(
                word for word in words
                if len(word) >= 3 and word not in STOPWORDS
            )

    # Start building the markdown output
    md_output = "# Tjedna analiza frekvencija riječi u hrvatskim medijima\n"
    for week_in_year in sorted(all_words_by_week.keys(), reverse=True):
        # Count occurrences of words for the week
        word_counts = Counter(all_words_by_week[week_in_year])
        TOP_WORDS = 100
        common_words = word_counts.most_common(TOP_WORDS)

        # Format the week identifier
        year, week = week_in_year.split('-W')
        year = int(year)
        week = int(week)
        md_output += f"\n## {week_in_year}\n\n```text\n"

        # Calculate max width for word-count display to align text
        max_width = max(len(f'{i}. {word}: {count}') for i, (word, count) in enumerate(common_words, 1))
        for i in range(0, TOP_WORDS, 4):
            row = []
            for j in range(4):
                if i + j < TOP_WORDS:
                    word, count = common_words[i + j]
                    # Format each word-count pair for alignment
                    row.append(f'{i+j+1}. {word}: {count}'.ljust(max_width))
                else:
                    row.append(''.ljust(max_width))
            md_output += ' '.join(row) + '\n'

        md_output += "```\n"

    # Write the formatted markdown to README.md
    with open('README.md', 'w') as f:
        f.write(md_output)
