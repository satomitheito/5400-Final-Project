import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_topic_vs_compound(data, title, color, country):
    plt.figure(figsize=(10, 6))
    plt.scatter(data['topic'], data['compound'], alpha=0.6, color=color)
    plt.title(title, fontsize=14)
    plt.xlabel('Topic', fontsize=12)
    plt.ylabel('Compound Score', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    fname = '../../plots/'+country+'_topic_compound_scatter.png'
    plt.savefig(fname)

def make_graphs(og_fpath, translated_fpath):
    all_articles = pd.read_csv(og_fpath)
    translated_article = pd.read_csv(translated_fpath)

    am_articles = all_articles[all_articles['Country'] == 'Japan']
    jp_articles = all_articles[all_articles['Country'] == 'US']

    # Analysis of sentiment by topic
    plot_topic_vs_compound(jp_articles, "Compound Scores by Topic (Japanese Articles)", color='blue', country='Japan')
    plot_topic_vs_compound(am_articles, "Compound Scores by Topic (English Articles)", color='red', country='America')
    plot_topic_vs_compound(all_articles, "Compound Scores by Topic (All Articles)", color='green', country='All')

    combined_avg_compound = all_articles.groupby(['topic', 'is_japanese'])['compound'].mean().unstack()
    combined_avg_compound.plot(kind='bar', figsize=(12, 6), title="Average Compound Score by Topic (Japanese vs English)")
    plt.xlabel("Topic")
    plt.ylabel("Average Compound Score")
    plt.legend(["English Articles", "Japanese Articles"], title="Language")
    plt.xticks(rotation=45)
    plt.savefig('../../plots/compare_topic_compound_scatter.png')

    # Analysis of sentiment by political bias
    # Plot for 'compound' sentiment
    sns.boxplot(data=jp_articles, x='bias', y='compound')
    plt.title('Distribution of Compound Sentiment by Bias In Japanese Articles')
    plt.savefig('../../plots/Japan_bias_compound_boxplot.png')

    sns.boxplot(data=am_articles, x='bias', y='compound')
    plt.title('Distribution of Compound Sentiment by Bias In American Articles')
    plt.savefig('../../plots/America_bias_compound_boxplot.png')

    plt.figure(figsize=(10, 6))
    sns.violinplot(data=all_articles, x='bias', y='compound', hue='Country', split=True)
    plt.title('Compound Sentiment by Bias and Country')
    plt.savefig('../../plots/compare_bias_compound_violin.png')

    # Analysis of sentiment of translated vs original
    translated_article['diff_compound'] = abs(translated_article['original_compound'] - translated_article['translated_compound'])

    # Distribution of compound sentiment differences
    plt.figure(figsize=(10, 6))
    sns.histplot(translated_article['diff_compound'], bins=30, kde=True, color='purple', alpha=0.8)
    plt.title('Distribution of Compound Sentiment Differences Across Translation', fontsize=16)
    plt.xlabel('Compound Sentiment Difference', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True)
    plt.savefig('../../plots/compare_translated_compound_hist.png')

    # Calculate average compound scores for original and translated texts by source
    avg_compound_scores = translated_article.groupby('source').agg({
        'original_compound': 'mean',
        'translated_compound': 'mean'
    }).reset_index()

    # Calculate the difference between original and translated compound scores
    avg_compound_scores['compound_diff'] = (
        avg_compound_scores['original_compound'] - avg_compound_scores['translated_compound']
    )

    x = np.arange(len(avg_compound_scores['source']))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot original and translated compound scores
    rects1 = ax.bar(x - width/2, avg_compound_scores['original_compound'], width, label='Original Compound')
    rects2 = ax.bar(x + width/2, avg_compound_scores['translated_compound'], width, label='Translated Compound')

    # Add labels, title, and custom x-axis tick labels
    ax.set_xlabel('Source', fontsize=14)
    ax.set_ylabel('Average Compound Score', fontsize=14)
    ax.set_title('Average Compound Scores by Source', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(avg_compound_scores['source'], rotation=45, fontsize=12)
    ax.legend()

    # Annotate the bars with the differences
    for i, diff in enumerate(avg_compound_scores['compound_diff']):
        ax.text(x[i], max(avg_compound_scores['original_compound'][i], avg_compound_scores['translated_compound'][i]) + 0.02,
                f'{diff:.2f}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('../../plots/compare_translated_bias_compound_hist.png')