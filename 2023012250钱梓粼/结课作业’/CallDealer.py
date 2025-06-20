@xml_parser_decorator
def print_protein_data(protein_data):
    for entry in protein_data:
        print("="*80)
        print(f"UniProt Entry: {entry['name']}")
        print("-"*80)
        print(f"Accession Numbers: {', '.join(entry['accessions'][:3])} [...] (Total: {len(entry['accessions'])})")
        print(f"\nProtein Information:")
        print(f"  Recommended Name: {entry['protein']['recommendedName']}")
        if entry['protein']['alternativeNames']:
            print(f"  Alternative Names: {', '.join(entry['protein']['alternativeNames'])}")
        
        print(f"\nGene: {entry['gene']}")
        
        org = entry['organism']
        print(f"\nOrganism:")
        print(f"  Scientific: {org['scientific']}")
        print(f"  Common: {org['common']}")
        print(f"  Taxonomy ID: {org['taxonomy']}")
        
        print(f"\nReferences (Count: {len(entry['references'])}):")
        for i, ref in enumerate(entry['references'][:3], 1):  # 只显示前3个
            print(f"  {i}. [{ref['type']}] {ref['title']}")
            print(f"     Authors: {', '.join(ref['authors'][:2])} [...]")
        
        if len(entry['references']) > 3:
            print(f"  ... and {len(entry['references'])-3} more references")
        print("="*80)
