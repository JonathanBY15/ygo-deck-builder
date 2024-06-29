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



// Submitting card search form with AJAX
document.getElementById('card-search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
        const query = new URLSearchParams(new FormData(event.target)).toString();
        const response = await fetch(`/api/cards/search?${query}`, { method: 'GET' });
        const result = await response.json();

        if (response.ok) {
            const searchResultContainer = document.querySelector('.search-result-container');
            searchResultContainer.innerHTML = '';

            result.cards.forEach(card => {
                const cardFrame = document.createElement('div');
                cardFrame.classList.add('card-frame');
                cardFrame.dataset.cardDescription = card.desc;
                cardFrame.innerHTML = `
                    <img src="${card.card_images[0].image_url_small}">
                    <div class="card-buttons-container container-fluid">
                        <div class="row">
                            <div class="col">
                                <i class="fa-solid fa-square-plus add-card-icon" data-card-id="${card.id}"></i>
                            </div>
                            <div class="col">
                                <i class="fa-solid fa-square-minus remove-card-icon" data-card-id="${card.id}"></i>
                            </div>
                        </div>
                    </div>
                `;
                searchResultContainer.appendChild(cardFrame);
            });

        } else {
            console.error('Error searching cards:', result.error);
            alert('Error searching cards. Please try again later.');
        }
    } catch (error) {
        console.error('Error searching cards:', error);
        alert('Error searching cards. Please try again later.');
    }
});

// Event delegation for adding and removing cards
document.addEventListener('click', async (event) => {
    const target = event.target;

    // Handling add card event
    if (target.classList.contains('add-card-icon')) {
        const deckId = getDeckIdFromUrl();
        const cardId = target.dataset.cardId;
        try {
            const response = await fetch(`/decks/${deckId}/cards/add/${cardId}`, { method: 'POST' });
            const result = await response.json();
            if (response.ok) {
                updateMainDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error adding card:', error);
        }
    }

    // Handling remove card event
    if (target.classList.contains('remove-card-icon')) {
        const deckId = getDeckIdFromUrl();
        const cardId = target.dataset.cardId;
        try {
            const response = await fetch(`/decks/${deckId}/cards/remove/${cardId}`, { method: 'POST' });
            const result = await response.json();
            if (response.ok) {
                updateMainDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error removing card:', error);
        }
    }
});


// Initial update when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const deckId = getDeckIdFromUrl();
    updateMainDeckGrid(deckId);
});


