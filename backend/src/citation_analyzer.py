import networkx as nx

class CitationAnalyzer:
    def __init__(self):
        self.citation_graph = nx.DiGraph()
    
    def build_citation_network(self, papers_data):
        """Builds a citation network from a list of paper data."""
        for paper in papers_data:
            # Ensure node metadata is a dictionary
            metadata = paper.get('metadata', {})
            if not isinstance(metadata, dict):
                metadata = {'title': str(metadata)}

            self.citation_graph.add_node(paper['id'], **metadata)
            
            # Ensure citations are a list
            citations = paper.get('citations', [])
            for citation in citations:
                # Add the cited paper as a node if it doesn't exist
                if not self.citation_graph.has_node(citation):
                    self.citation_graph.add_node(citation, title="External Citation")
                self.citation_graph.add_edge(paper['id'], citation)
    
    def calculate_impact_metrics(self):
        """Calculates PageRank and betweenness centrality for the network."""
        if not self.citation_graph.nodes():
            print("Citation graph is empty. Cannot calculate metrics.")
            return {}, {}

        pagerank = nx.pagerank(self.citation_graph)
        betweenness = nx.betweenness_centrality(self.citation_graph)
        return pagerank, betweenness

if __name__ == '__main__':
    # Sample data representing academic papers and their citations
    sample_papers = [
        {'id': 'paper_A', 'metadata': {'title': 'Paper A', 'year': 2020}, 'citations': ['paper_B', 'paper_C']},
        {'id': 'paper_B', 'metadata': {'title': 'Paper B', 'year': 2018}, 'citations': ['paper_C']},
        {'id': 'paper_C', 'metadata': {'title': 'Paper C', 'year': 2015}, 'citations': []},
        {'id': 'paper_D', 'metadata': {'title': 'Paper D', 'year': 2021}, 'citations': ['paper_A']}
    ]

    analyzer = CitationAnalyzer()
    analyzer.build_citation_network(sample_papers)

    print("--- Citation Network Analysis ---")
    print(f"Nodes (Papers): {list(analyzer.citation_graph.nodes())}")
    print(f"Edges (Citations): {list(analyzer.citation_graph.edges())}")

    pagerank, betweenness = analyzer.calculate_impact_metrics()

    print("\n--- Impact Metrics ---")
    print("PageRank:")
    for paper, score in pagerank.items():
        print(f"  {paper}: {score:.4f}")

    print("\nBetweenness Centrality:")
    for paper, score in betweenness.items():
        print(f"  {paper}: {score:.4f}")
