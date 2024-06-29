// Scripts will be written here

// FUNCTION to FETCH the deck's cards and UPDATE THE MAIN DECK GRID
async function updateMainDeckGrid(deckId) {
    try {
        const response = await fetch(`/api/decks/${deckId}/cards`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const deckCards = await response.json();

        // Reset the grid
        for (let i = 1; i <= 60; i++) {
            const cardImg = document.getElementById(`main-card-img-${i}`);
            cardImg.src = '/static/images/placeholder.png';
            cardImg.parentElement.dataset.cardDescription = '';
        }

        // Update the grid with deck's cards
        let cardIndex = 0;
        deckCards.forEach(card => {
            for (let i = 0; i < card.quantity; i++) {
                const row = Math.floor(cardIndex / 15);
                const col = cardIndex % 4;
                cardImg = document.getElementById(`main-card-img-${cardIndex + 1}`)
                cardImg.src = card.img_url;
                cardImg.parentElement.dataset.cardDescription = card.card_desc;
                cardIndex++;
            }
        });

    } catch (error) {
        console.error('Error fetching deck cards:', error);
    }
}



// Event listeners for adding cards using AJAX
document.querySelectorAll('.add-card-icon').forEach(button => {
    button.addEventListener('click', async (event) => {
        const deckId = getDeckIdFromUrl();
        const cardId = button.dataset.cardId;
        try {
            const response = await fetch(`/decks/${deckId}/cards/add/${cardId}`, { method: 'POST' });
            const result = await response.json();
            if (response.ok) {
                // alert(result.message);
                updateMainDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error adding card:', error);
        }
    });
});


// Event listeners for removing cards using AJAX
document.querySelectorAll('.remove-card-icon').forEach(button => {
    button.addEventListener('click', async (event) => {
        const deckId = getDeckIdFromUrl();;
        const cardId = button.dataset.cardId;
        try {
            const response = await fetch(`/decks/${deckId}/cards/remove/${cardId}`, { method: 'POST' });
            const result = await response.json();
            if (response.ok) {
                // alert(result.message);
                updateMainDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error removing card:', error);
        }
    });
});


// HOVER EFFECTS (View Card and Description)

// Event listener for displaying the card IMAGE in 'card-view' when hovering over a card in the MAIN DECK
document.querySelectorAll('.main-card-slot').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardImg = cardSlot.querySelector('img'); // Get the image inside the cardSlot
        if (cardImg) {
            document.querySelector('.card-view').src = cardImg.src; // Set the image source to the source of the image inside the cardSlot
        }
    });
});


// Event listener for displaying the card DESCRIPTION in 'description' when hovering over a card in the MAIN DECK
document.querySelectorAll('.main-card-slot').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardDescription = cardSlot.dataset.cardDescription; // Get the description from the cardSlot's data attribute
        document.querySelector('.description').textContent = cardDescription; // Set the description text to the cardDescription
    });
});

// Event listener for displaying the card IMAGE in 'card-view' when hovering over a card in the SEARCH RESULTS
document.querySelectorAll('.card-frame').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardImg = cardSlot.querySelector('img'); // Get the image inside the cardSlot
        if (cardImg) {
            document.querySelector('.card-view').src = cardImg.src; // Set the image source to the source of the image inside the cardSlot
        }
    });
});

// Event listener for displaying the card DESCRIPTION in 'description' when hovering over a card in the SEARCH RESULTS
document.querySelectorAll('.card-frame').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardDescription = cardSlot.dataset.carddescription; // Get the description from the cardSlot's data attribute
        document.querySelector('.description').textContent = cardDescription; // Set the description text to the cardDescription
    });
});



// Function to extract deckId from the URL
function getDeckIdFromUrl() {
    const urlParts = window.location.pathname.split('/');
    return urlParts[urlParts.length - 1];
}


// Add AJAX to clear deck
document.querySelector('#clear-deck').addEventListener('click', async (event) => {
    const deckId = getDeckIdFromUrl();
    try {
        const response = await fetch(`/api/decks/${deckId}/clear`, { method: 'POST' });
        const result = await response.json();
        if (response.ok) {
            // alert(result.message);
            updateMainDeckGrid(deckId);
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error clearing deck:', error);
    }
});





// // Add AJAX to next and previous buttons
// // Function to handle form submission via AJAX
// const handleFormSubmission = async (form) => {
//     try {
//         const formData = new FormData(form);
//         const deckId = getDeckIdFromUrl(); // Ensure you have a way to get deck_id if needed
//         const url = form.getAttribute('action'); // Get the form action URL

//         const response = await fetch(url, {
//             method: 'POST',
//             body: formData
//         });

//         if (!response.ok) {
//             throw new Error('Failed to load page');
//         }

//         const data = await response.json();
//         // Handle the response data as needed (e.g., update the search results)
//         updateSearchResults(data); // Example function to update search results

//     } catch (error) {
//         console.error('Error loading page:', error);
//         // Handle error (e.g., show an alert)
//         alert('Failed to load page');
//     }
// };

// // Event listener for next page form submission
// const nextPageForm = document.getElementById('nextPageForm');
// if (nextPageForm) {
//     nextPageForm.addEventListener('submit', (event) => {
//         event.preventDefault(); // Prevent the default form submission
//         handleFormSubmission(nextPageForm); // Call function to handle AJAX submission
//     });
// }

// // Event listener for previous page form submission
// const prevPageForm = document.querySelector('form[action$="/cards/previous_page"]');
// if (prevPageForm) {
//     prevPageForm.addEventListener('submit', (event) => {
//         event.preventDefault(); // Prevent the default form submission
//         handleFormSubmission(prevPageForm); // Call function to handle AJAX submission
//     });
// }






// Initial update when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const deckId = getDeckIdFromUrl();
    updateMainDeckGrid(deckId);
});


