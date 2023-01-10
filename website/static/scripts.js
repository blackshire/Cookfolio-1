
/* for ingredients list on recipe.html */
const listItems = document.querySelectorAll('.list-group-item');

listItems.forEach(item => {
  item.addEventListener('click', () => {
    item.classList.toggle('done');
  });
});


/* for adding and removing ingredients to a new recipe */
const ingredientsContainer = document.getElementById('ingredients');

document.addEventListener('click', event => {
  if (event.target.classList.contains('add-ingredient')) {
    const ingredientRow = event.target.parentElement.parentElement;
    const newIngredientRow = ingredientRow.cloneNode(true);
    newIngredientRow.querySelector('input#ingredient-number').value = '';
    newIngredientRow.querySelector('select#ingredient-unit').value = 'teaspoon';
    newIngredientRow.querySelector('input#ingredient-description').value = '';
    ingredientsContainer.appendChild(newIngredientRow);
  }
});

document.querySelector('#ingredients').addEventListener('click', function(event) {
  if (event.target.classList.contains('remove-ingredient')) {
    // Get the parent element of the remove button (the ingredient element)
    const ingredientElement = event.target.parentElement.parentElement;

    // Check if there is more than one ingredient element
    if (document.querySelectorAll('.ingredient').length > 1) {
      // Remove the ingredient element if there is more than one
      ingredientElement.remove();
    }
  }
});




