import click

from network_analyzer.ai_network_analyzer import AiAnalyzer
from network_analyzer.threshold_network_analyzer import ThresholdAnalyzer

@click.command()
@click.option('-t','--analyzer-type', type=click.Choice(['ai', 'legacy'], case_sensitive=False), default='ai', help='Select analyzer type. AI or legacy')
@click.option('--data-source', type=click.Choice(['prometheus'], case_sensitive=False), default='prometheus', help='Select data source. Currently only Prometheus available.')
def run_analyzer(analyzer_type, data_source):
    if analyzer_type == 'ai':
        Analyzer = AiAnalyzer
    else:
        Analyzer = ThresholdAnalyzer
    analyzer =Analyzer() # TODO add params
    print(analyzer)

if __name__ == '__main__':
    run_analyzer()