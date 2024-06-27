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






// Function to fetch the deck's cards and update the grid
async function updateMainDeckGrid(deckId) {
    try {
        const response = await fetch(`/api/decks/${deckId}/cards`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const deckCards = await response.json();

        // Clear the grid
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 15; col++) {
                document.getElementById(`main-card-img-${(row * 15) + (col + 1)}`).src = '/static/images/placeholder.png';
            }
        }

        // Update the grid with deck's cards
        let cardIndex = 0;
        deckCards.forEach(card => {
            for (let i = 0; i < card.quantity; i++) {
                const row = Math.floor(cardIndex / 15);
                const col = cardIndex % 4;
                document.getElementById(`main-card-img-${cardIndex + 1}`).src = card.img_url;
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
