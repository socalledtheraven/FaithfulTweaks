function sortCategories() {
    console.log("Sorting categories...");

    // 1. Select the container of all the category divs.
    //    Assumes all .category divs are direct children of this container.
    //    If they are scattered, this needs adjustment.
    const container = document.getElementById('packs-selector');
    if (!container) {
        console.error("Error: Container with ID 'categories-container' not found.");
        return;
    }

    // 2. Select all the category divs within the container.
    const categories = container.querySelectorAll('div.category');
    if (categories.length === 0) {
        console.warn("No 'div.category' elements found within the container.");
        return;
    }

    // 3. Convert the NodeList to an Array to use the sort method.
    const categoriesArray = Array.from(categories);

    // 4. Sort the array.
    categoriesArray.sort((a, b) => {
      // Find the h4 header within each category div
      const h4a = a.querySelector('h4.header');
      const h4b = b.querySelector('h4.header');

      // Get the text content, provide default empty string if h4 not found
      const textA = h4a ? h4a.textContent.trim() : '';
      const textB = h4b ? h4b.textContent.trim() : '';

      // Use localeCompare for proper alphabetical sorting (handles case, accents etc.)
      return textA.localeCompare(textB);
    });

    // 5. Re-append the sorted elements back into the container.
    //    Appending an element that is already in the DOM moves it.
    //    By appending them in the sorted order, they end up in the correct sequence.
    categoriesArray.forEach(category => {
      container.appendChild(category);
    });

    console.log("Categories sorted and reordered.");
  }

sortCategories();