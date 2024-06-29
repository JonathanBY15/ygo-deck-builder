// Scripts will be written here

// Function to extract deckId from the URL
function getDeckIdFromUrl() {
    const urlParts = window.location.pathname.split('/');
    return urlParts[urlParts.length - 1];
}

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


// HOVER EFFECTS (View Card and Description)
document.addEventListener('mouseover', (event) => {
    const target = event.target;

    // Main deck cards hover effect
    if (target.matches('.main-card-slot img')) {
        const cardImgSrc = target.src;
        document.querySelector('.card-view').src = cardImgSrc;

        const cardDescription = target.closest('.main-card-slot').dataset.cardDescription;
        document.querySelector('.description').textContent = cardDescription;
    }

    // Search result cards hover effect
    if (target.matches('.card-frame img')) {
        const cardImgSrc = target.src;
        document.querySelector('.card-view').src = cardImgSrc;

        const cardDescription = target.closest('.card-frame').dataset.cardDescription;
        document.querySelector('.description').textContent = cardDescription;
    }
});


// Initial update when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const deckId = getDeckIdFromUrl();
    updateMainDeckGrid(deckId);
});


