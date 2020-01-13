import argparse
from src import main
from src.constants import Labels

def display(articles):
    color_reset = "\033[0m"
    for idx, article in enumerate(articles[:args.n]):
        if article.score < 0.25:
            color = "\033[91m"
        elif article.score < 0.4:
            color = "\033[33m"
        else:
            color = "\033[32m"
        score = f"{color} {article.score} {color_reset}"
        print(f"[{idx}] {score} [{article.source_page}] {article.text}")

parser = argparse.ArgumentParser(description='Rss news reader')

parser.add_argument("--negative", type=int, nargs="+",metavar="N")
parser.add_argument("--positive", type=int, nargs="+",metavar="N")
parser.add_argument("--open", type=int, nargs="+",metavar="N")
parser.add_argument("--n", type=int, default=30)
parser.add_argument("--update", action="store_true")
parser.add_argument("--train", action="store_true")
parser.add_argument("--update-scores", action="store_true")
parser.add_argument("--unlabeled", action="store_true")

args = parser.parse_args()

if args.update:
    main.update()
    main.list_articles()
if args.negative:
    main.annotate(args.negative, Labels.NEGATIVE)
elif args.positive:
    main.annotate(args.positive, Labels.POSITIVE)
elif args.open:
    main.open(args.open)
elif args.train:
    main.train()
elif args.update_scores:
    main.update_scores()
elif args.unlabeled:
    articles = main.unlabeled()
    display(articles)
else:
    latest_articles = main.list_articles()
    display(latest_articles)
