def check_request(max_needs, current_needs, available_resources, allocated_resources, request, process):
    """
    Check if the request can be safely granted using the Banker's algorithm.
    
    Parameters:
        max_needs (list of lists): Maximum resource needs for each process.
        current_needs (list of lists): Current resource needs for each process.
        available_resources (list): Available resources.
        allocated_resources (list of lists): Allocated resources for each process.
        request (list): Requested resources.
        process (int): Process number making the request.
    
    Returns:
        (bool, list, list of lists, list of lists, str): Tuple containing whether the request is safe,
                                                         new available resources,
                                                         new allocated resources,
                                                         new current needs,
                                                         and a message.
    """
    # Validate the request
    if any(request[i] > current_needs[process][i] for i in range(len(request))):
        return False, available_resources, allocated_resources, current_needs, "Error: Request exceeds maximum needs"
    
    if any(request[i] > available_resources[i] for i in range(len(request))):
        return False, available_resources, allocated_resources, current_needs, "Error: Request exceeds available resources"
    
    # Attempt allocation
    new_available = [available_resources[i] - request[i] for i in range(len(available_resources))]
    new_allocated = [row[:] for row in allocated_resources]
    new_needs = [row[:] for row in current_needs]
    
    for i in range(len(request)):
        new_allocated[process][i] += request[i]
        new_needs[process][i] -= request[i]
    
    # Safety check
    work = new_available[:]
    finish = [False] * len(max_needs)
    sequence = []
    
    while True:
        found = False
        for i in range(len(max_needs)):
            if not finish[i] and all(new_needs[i][j] <= work[j] for j in range(len(work))):
                work = [work[j] + new_allocated[i][j] for j in range(len(work))]
                finish[i] = True
                sequence.append(i)
                found = True
                break
        
        if not found:
            break
    
    if all(finish):
        return True, new_available, new_allocated, new_needs, f"Safe sequence: {sequence}"
    else:
        return False, available_resources, allocated_resources, current_needs, "Warning: Allocation leads to an unsafe state"


def display_matrix(title, matrix):
    """Display a matrix with a title."""
    print(f"\n{title}:")
    for row in matrix:
        print(" ".join(f"{elem:>3}" for elem in row))


# Example usage
if __name__ == "__main__":
    # Input data
    max_needs = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    
    allocated_resources = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    current_needs = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    
    available_resources = [3, 3, 2]
    
    # Process 1 requests [1, 0, 2]
    request = [1, 0, 2]
    process = 1
    
    # Execute Banker's algorithm
    is_safe, avail, alloc, needs, msg = check_request(max_needs, current_needs, available_resources, allocated_resources, request, process)
    
    # Output results
    print("\nBanker's Algorithm Result:")
    print(f"Can the request be granted: {'Yes' if is_safe else 'No'}")
    print(f"Message: {msg}")
    
    if is_safe:
        print("\nState after allocation:")
        print("Available:", " ".join(map(str, avail)))
        display_matrix("Max Needs", max_needs)
        display_matrix("Allocated Resources", alloc)
        display_matrix("Current Needs", needs)