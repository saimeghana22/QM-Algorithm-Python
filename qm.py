# Function to read a PLA file and extract the number of inputs, outputs, and the truth table data
def read_pla_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines in the file

    input_count = 0  # Number of inputs in the logic function
    output_count = 0  # Number of outputs in the logic function
    truth_table = []  # Store the truth table (input-output pairs)

    # Process each line to extract relevant data
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith(".i"):
            input_count = int(line.split()[1])  # Get number of inputs
        elif line.startswith(".o"):
            output_count = int(line.split()[1])  # Get number of outputs
        elif line and not line.startswith("."):
            truth_table.append(line.split())  # Add the input-output pair to the truth table

    return input_count, output_count, truth_table

# Function to apply the Quine-McCluskey algorithm for logic minimization
def minimize_logic_using_quine_mccluskey(truth_table):
    # Step 1: Group the minterms based on the number of 1's in their binary representation
    minterms = [term for term in truth_table if term[1] == '1']  # Focus on the minterms where output is 1
    grouped_terms = {}

    # Group terms by the number of 1's they contain in their binary representation
    for term in minterms:
        binary_term = term[0]
        ones_count = binary_term.count('1')
        if ones_count not in grouped_terms:
            grouped_terms[ones_count] = []  # Initialize the group if it doesn't exist
        grouped_terms[ones_count].append(binary_term)

    # Step 2: Combine terms that differ by exactly one bit
    def combine_terms(term1, term2):
        difference_count = 0
        combined_term = []
        for i in range(len(term1)):
            if term1[i] != term2[i]:
                difference_count += 1
                combined_term.append('-')  # Replace the differing bit with '-'
            else:
                combined_term.append(term1[i])
        return ''.join(combined_term) if difference_count == 1 else None

    prime_implicants = set()  # To store the resulting prime implicants

    # Function to combine terms from adjacent groups
    def combine_adjacent_groups(grouped_terms):
        new_grouped_terms = {}
        combined_terms = set()
        used_terms = set()

        # Combine terms from adjacent groups where only one bit differs
        for ones_count in sorted(grouped_terms.keys()):
            if (ones_count + 1) in grouped_terms:  # Check if the next group exists
                for term1 in grouped_terms[ones_count]:
                    for term2 in grouped_terms[ones_count + 1]:
                        combined_term = combine_terms(term1, term2)
                        if combined_term:
                            combined_terms.add(combined_term)  # Add the combined term
                            used_terms.update([term1, term2])  # Mark terms as used

        # Add all terms that weren't combined to the prime implicants set
        for terms in grouped_terms.values():
            for term in terms:
                if term not in used_terms:
                    prime_implicants.add(term)

        # Group combined terms by the number of 1's for further processing
        for term in combined_terms:
            ones_count = term.count('1')
            if ones_count not in new_grouped_terms:
                new_grouped_terms[ones_count] = []
            new_grouped_terms[ones_count].append(term)

        return new_grouped_terms, prime_implicants

    # Continuously combine terms until no more combinations are possible
    while True:
        new_grouped_terms, new_prime_implicants = combine_adjacent_groups(grouped_terms)
        if not new_grouped_terms:  # If no new groups are formed, stop
            break
        prime_implicants.update(new_prime_implicants)
        grouped_terms = new_grouped_terms

    # Return the minimized terms (prime implicants)
    minimized_terms = [(term, '1') for term in prime_implicants]
    return minimized_terms

# Function to write the minimized logic to a new PLA file
def write_minimized_logic_to_pla(file_path, input_count, output_count, minimized_terms):
    with open(file_path, 'w') as file:
        file.write(f".i {input_count}\n")  # Write the number of inputs
        file.write(f".o {output_count}\n")  # Write the number of outputs
        for term in minimized_terms:
            file.write(f"{term[0]} {term[1]}\n")  # Write the minimized terms
        file.write(".e\n")  # End the PLA file

# Main function to run the program
def main(input_pla_path, output_pla_path):
    input_count, output_count, truth_table = read_pla_file(input_pla_path)  # Parse the input PLA file
    minimized_terms = minimize_logic_using_quine_mccluskey(truth_table)  # Minimize the logic
    write_minimized_logic_to_pla(output_pla_path, input_count, output_count, minimized_terms)  # Write the result

# Entry point of the program
if __name__ == "__main__":
    input_file_path = r"C:\Users\R.SAI MEGHANA\OneDrive\Desktop\project\input.pla"  # Path to the input PLA file
    output_file_path = r"C:\Users\R.SAI MEGHANA\OneDrive\Desktop\project\output_minimized.pla"  # Path for the output PLA file

    main(input_file_path, output_file_path)  # Run the main function
