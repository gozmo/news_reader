#!/usr/bin/env python3
import argparse
from src import main
from src.constants import Labels

def score_string(score):
    color_reset = "\033[0m"
    if score < 0.3:
        color = "\033[91m"
    elif score < 0.5:
        color = "\033[33m"
    else:
        color = "\033[32m"
    score = f"{color} {score} {color_reset}"
    return score

def display(articles, source, n):
    for idx, article in enumerate(articles[:n], 0):
        score = score_string(article.score)
        text = article.text.replace("\n", " ")

        print(f"[{idx}] {score} {article.source}, {text}")

def setup_parser(parser):
    parser.add_argument("--negative", type=int, nargs="+",metavar="N")
    parser.add_argument("--positive", type=int, nargs="+",metavar="N")
    parser.add_argument("--open", type=int, nargs="+",metavar="N")
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--update", action="store_true", default=False)
    parser.add_argument("--train", action="store_true", default=False)
    parser.add_argument("--update-scores", action="store_true", default=False)
    parser.add_argument("--unlabeled", action="store_true", default=False)
    parser.add_argument("--all", action="store_true", default=False)



parser = argparse.ArgumentParser(description='Rss news reader')
parser.add_argument("--init", action="store_true")

sub_parsers = parser.add_subparsers(dest="source")

twitter_parser = sub_parsers.add_parser("twitter")
setup_parser(twitter_parser)
news_parser = sub_parsers.add_parser("news")
setup_parser(news_parser)
blog_parser = sub_parsers.add_parser("blogs")
setup_parser(blog_parser)

args = parser.parse_args()
print(args)

if args.source is None:
    for source in ["twitter", "news"]:
        print(f"## {source} ##")
        latest_articles = main.list_articles(source, "latest", False)
        display(latest_articles, source, 10)
elif args.init:
    main.init()
elif args.update:
    main.update(args.source)
    main.list_articles(args.source, "latest", False)
elif args.negative:
    main.annotate(args.source, args.negative, Labels.NEGATIVE)
elif args.positive:
    main.annotate(args.source, args.positive, Labels.POSITIVE)
elif args.open:
    main.open(args.source, args.open)
elif args.train:
    main.train(args.source)
elif args.update_scores:
    main.update_scores(args.source)
elif args.unlabeled:
    articles = main.unlabeled(args.source)
    display(articles, args.source, 20)
elif args.source:
    latest_articles = main.list_articles(args.source, "latest", args.all)
    display(latest_articles, args.source, 20)
else:
    pass
