import requests
from bs4 import BeautifulSoup

def print_grid_from_doc_table(doc_url):

    # First, get the page and use a parser to look at the html
    response = requests.get(doc_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # You need to find the table class, as it can change (can verify manually with inspect -> element and
    # will be shown as <table class="c8", for example)
    # this helps locate it
    table = soup.find("table")
    
    # Extract the class for later use
    # Check to ensure table was actually found
    if table:
        table_class = table.get("class")
        if table_class:
            table_class = " ".join(table_class)
    else:
        print("Table class not found")
        return
    
    # Now get use the class type to find the table with the html
    # If class type is not being properly used, or not properly found, error should print with details
    # of class type being used
    table = soup.find("table", class_=table_class)
    if not table:
        print(f"Table not found using class {table_class}")
        return

    # Now, identify each row
    # Because values can be either double or single digit, rows must be identified
    # looking at the html, each row begins with "tr"
    rows = table.find_all("tr")

    # Dictionary for storing points
    # max values for x and y to keep track of grid size needed
    points = {}
    max_x = 0
    max_y = 0

    for row in rows:
        # There are three cells per row, each starting with "td"
        cells = row.find_all("td")

        # The order is x, character, y
        # so extract the cell values/character in that order
        # use get_text to strip out the html tags
        x_str = cells[0].get_text(strip=True)
        char_str = cells[1].get_text(strip=True)
        y_str = cells[2].get_text(strip=True)

        # Now need to convert to integers
        # ignore values that can't be parsed
        try:
            x = int(x_str)
            y = int(y_str)
        except ValueError:
            continue

        # Now store the character value as assigned to the coordinates
        points[(x, y)] = char_str

        # Update maximum x and y values for grid size
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    # check to make sure values actually were added to the dictionary,
    # gives message if nothing was added
    if not points:
        print("No valid (x,y) points found in the table.")
        return

    # Build the empty grid, a list of lists with proper dimensions (adding 1 to the maximums)
    width = max_x + 1
    height = max_y + 1
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Fill in the grid with the characters at each designated coordinate
    for (x, y), ch in points.items():
        grid[y][x] = ch

    # Finally, print the grid
    # make sure to print "reversed" as so that letters are not upside down 
    # (as you would notice when printing the "F" demo)
    for row in reversed(grid):
        print("".join(row))


# Add in the URL and use the function
doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
print_grid_from_doc_table(doc_url)
