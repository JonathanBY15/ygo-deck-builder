// Scripts will be written here

// ADD CARD TO DECK
function addCardToDeck(deckId, cardId) {
    $.ajax({
        url: `/decks/${deckId}/cards/add/${cardId}`,
        type: 'POST',
        success: function (response) {
            // Optionally handle success, e.g., update the UI to reflect the added card
            alert('Card added successfully!');
        },
        error: function (xhr, status, error) {
            // Handle error
            alert('Error adding card: ' + error);
        }
    });
}



// REMOVE CARD FROM DECK
function removeCardFromDeck(deckId, cardId) {
    $.ajax({
        url: `/decks/${deckId}/cards/remove/${cardId}`,
        type: 'POST',
        success: function (response) {
            // Optionally handle success, e.g., update the UI to reflect the removed card
            alert('Card removed successfully!');
        },
        error: function (xhr, status, error) {
            // Handle error
            alert('Error removing card: ' + error);
        }
    });
}


// FUNCTION to FETCH the deck's cards and UPDATE THE MAIN DECK GRID
async function updateMainDeckGrid(deckId) {
    try {
        const response = await fetch(`/api/decks/${deckId}/cards`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const deckCards = await response.json();

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

// Event listener for displaying the card image in 'card-view' when hovering over a card in the main deck
document.querySelectorAll('.main-card-slot').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardImg = cardSlot.querySelector('img'); // Get the image inside the cardSlot
        if (cardImg) {
            document.querySelector('.card-view').src = cardImg.src; // Set the image source to the source of the image inside the cardSlot
        }
    });
});

// Event listener for displaying the card description in 'description' when hovering over a card in the main deck
document.querySelectorAll('.main-card-slot').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardDescription = cardSlot.dataset.cardDescription; // Get the description from the cardSlot's data attribute
        document.querySelector('.description').textContent = cardDescription; // Set the description text to the cardDescription
    });
});

// Event listener for displaying the card image in 'card-view' when hovering over a card in the search results
document.querySelectorAll('.card-frame').forEach(cardSlot => {
    cardSlot.addEventListener('mouseover', (event) => {
        const cardImg = cardSlot.querySelector('img'); // Get the image inside the cardSlot
        if (cardImg) {
            document.querySelector('.card-view').src = cardImg.src; // Set the image source to the source of the image inside the cardSlot
        }
    });
});





// Function to extract deckId from the URL
function getDeckIdFromUrl() {
    const urlParts = window.location.pathname.split('/');
    return urlParts[urlParts.length - 1];
}

// Initial update when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const deckId = getDeckIdFromUrl();
    updateMainDeckGrid(deckId);
});
