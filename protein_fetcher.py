import requests
def fetch_uniprot_data(size, query, make_fasta = None, make_fast_name = None):
    # URL for UniProt API
    url = "https://rest.uniprot.org/uniprotkb/search"

    # Query parameters
    params = {
        "query": query,  # 
        "size": size,
        "format": "json"  # Get results in JSON format
    }

    # Send GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        return


    if "results" in data:
        if make_fasta.upper() == "Y":
            with open(make_fast_name, "w") as fasta_file:
                for entry in data["results"]:
                    accession = entry["primaryAccession"]
                    protein_name = entry["proteinDescription"]["recommendedName"]["fullName"]["value"]
                    organism = entry["organism"]["scientificName"]
                    length = entry["sequence"]["length"]
                    sequence = entry["sequence"]["value"]
                    fasta_file.write(f">{protein_name}-{organism}\n")
                    for i in range(0, len(sequence), 80):
                        fasta_file.write(sequence[i:i+80] + "\n")

        elif make_fasta == "n" or "N":
            for entry in data["results"]:
                    accession = entry["primaryAccession"]
                    protein_name = entry["proteinDescription"]["recommendedName"]["fullName"]["value"]
                    organism = entry["organism"]["scientificName"]
                    length = entry["sequence"]["length"]
                    sequence = entry["sequence"]["value"]
                
                    print(f"Accession: {accession}")
                    print(f"Protein Name: {protein_name}")
                    print(f"Organism: {organism}")
                    print(f"Sequence Length: {length}")
                    print(f"sequence: {sequence}")
                    print("-" * 40)

    else:
        print("No results found.")
def main():
    size = input("Please give the amount of hits you would like to have:  ")
    query = input("Please give the query you would like to search uniprot with:  ")
    make_fasta = input("Generate a FASTA file for all the hits? [Y/N]:  ")
    print(make_fasta)
    if make_fasta.upper() == "Y":
        fasta_file_name = input("Please name the FASTA file:  ")
        fasta_file_name = fasta_file_name + ".FASTA"
        fetch_uniprot_data(size, query, make_fasta, fasta_file_name)
    else:
        fetch_uniprot_data(size, query, make_fasta)


    

if __name__ == "__main__":
    main()

