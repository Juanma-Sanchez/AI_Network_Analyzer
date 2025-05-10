import click

from network_analyzer.ai_network_analyzer import AiAnalyzer
from network_analyzer.legacy_network_analyzer import LegacyAnalyzer

@click.command()
@click.option('-t','--analyzer-type', type=click.Choice(['ai', 'legacy'], case_sensitive=False), default='ai', help='Select analyzer type. AI or legacy')
def run_analyzer(analyzer_type):
    if analyzer_type == 'ai':
        analyzer = AiAnalyzer()
    else:
        analyzer = LegacyAnalyzer()

if __name__ == '__main__':
    run_analyzer()