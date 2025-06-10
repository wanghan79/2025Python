import argparse
import xml.etree.ElementTree as ET

def build_hierarchy(node, path=""):
    """Recursively build the tag hierarchy."""
    current_path = f"{path}/{node.tag}" if path else node.tag
    hierarchy = {}
    
    # Process all child nodes
    for child in node:
        child_tag = child.tag
        if child_tag not in hierarchy:
            hierarchy[child_tag] = build_hierarchy(child, current_path)
        else:
            # Merge trees with the same tag
            hierarchy[child_tag] = merge_hierarchies(hierarchy[child_tag], build_hierarchy(child, current_path))
    
    # Treat attributes as special "tags"
    for attr in node.attrib:
        attr_tag = f"@{attr}"
        hierarchy[attr_tag] = {}
    
    return {node.tag: hierarchy}

def merge_hierarchies(hierarchy1, hierarchy2):
    """Merge two hierarchies, preserving all unique paths."""
    merged = {}
    
    # Merge first-level tags
    for tag in set(hierarchy1.keys()).union(hierarchy2.keys()):
        if tag in hierarchy1 and tag in hierarchy2:
            merged[tag] = merge_hierarchies(hierarchy1[tag], hierarchy2[tag])
        elif tag in hierarchy1:
            merged[tag] = hierarchy1[tag]
        else:
            merged[tag] = hierarchy2[tag]
    
    return merged

def display_hierarchy(hierarchy, indent=0):
    """Format and print the tag hierarchy."""
    for tag, children in hierarchy.items():
        print("  " * indent + tag)
        display_hierarchy(children, indent + 1)

def main():
    parser = argparse.ArgumentParser(description='Generate the tag hierarchy of an XML file.')
    parser.add_argument('xml_file', help='Path to the XML file.')
    args = parser.parse_args()
    
    try:
        # Parse the XML file
        tree = ET.parse(args.xml_file)
        root = tree.getroot()
        
        # Build the tag hierarchy
        hierarchy = build_hierarchy(root)
        
        # Print the tag hierarchy
        print(f"Tag hierarchy of XML file '{args.xml_file}':")
        display_hierarchy(hierarchy)
        
    except FileNotFoundError:
        print(f"Error: File '{args.xml_file}' not found.")
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
    except Exception as e:
        print(f"An unknown error occurred: {e}")

if __name__ == "__main__":
    main()