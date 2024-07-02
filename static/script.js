
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
            if (!card.is_extra_deck) {
                for (let i = 0; i < card.quantity; i++) {
                    const row = Math.floor(cardIndex / 15);
                    const col = cardIndex % 4;
                    cardImg = document.getElementById(`main-card-img-${cardIndex + 1}`)
                    cardImg.src = card.img_url;
                    cardImg.parentElement.dataset.cardDescription = card.card_desc;
                    cardImg.parentElement.dataset.cardId = card.id;
                    cardIndex++;
                }

            }
        });

    } catch (error) {
        console.error('Error fetching deck cards:', error);
    }
}

// FUNCTION to FETCH the deck's cards and UPDATE THE EXTRA DECK GRID
async function updateExtraDeckGrid(deckId) {
    try {
        const response = await fetch(`/api/decks/${deckId}/cards`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const deckCards = await response.json();

        // Reset the grid
        for (let i = 1; i <= 15; i++) {
            const cardImg = document.getElementById(`extra-card-img-${i}`);
            cardImg.src = '/static/images/placeholder.png';
            cardImg.parentElement.dataset.cardDescription = '';
        }

        // Update the grid with deck's cards
        let cardIndex = 0;
        deckCards.forEach(card => {
            console.log(card);
            if (card.is_extra_deck) {
                for (let i = 0; i < card.quantity; i++) {
                    const row = Math.floor(cardIndex / 15);
                    const col = cardIndex % 4;
                    cardImg = document.getElementById(`extra-card-img-${cardIndex + 1}`)
                    cardImg.src = card.img_url;
                    cardImg.parentElement.dataset.cardDescription = card.card_desc;
                    cardImg.parentElement.dataset.cardId = card.id;
                    cardIndex++;
                }
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
            updateExtraDeckGrid(deckId);
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error clearing deck:', error);
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
                updateExtraDeckGrid(deckId);
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
                updateExtraDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error removing card:', error);
        }
    }
});


// Let user remove card from main deck by clicking on the card
document.addEventListener('click', async (event) => {
    const target = event.target;
    if ((target.matches('.main-card-slot img') && target.closest('.main-card-slot').dataset.cardId)) {
        const deckId = getDeckIdFromUrl();
        const cardId = target.closest('.main-card-slot').dataset.cardId;
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

// Let user remove card from extra deck by clicking on the card
document.addEventListener('click', async (event) => {
    const target = event.target;
    if ((target.matches('.extra-card-slot img') && target.closest('.extra-card-slot').dataset.cardId)) {
        const deckId = getDeckIdFromUrl();
        const cardId = target.closest('.extra-card-slot').dataset.cardId;
        try {
            const response = await fetch(`/decks/${deckId}/cards/remove/${cardId}`, { method: 'POST' });
            const result = await response.json();
            if (response.ok) {
                updateExtraDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error removing card:', error);
        }
    }
});

// Let user add card from search results by clicking on the card
document.addEventListener('click', async (event) => {
    const target = event.target;
    if (target.matches('.card-frame img') && target.closest('.card-frame').dataset.cardId) {
        const deckId = getDeckIdFromUrl();
        const cardId = target.closest('.card-frame').dataset.cardId;
        try {
            const response = await fetch(`/decks/${deckId}/cards/add/${cardId}`, { method: 'POST' });
            const result = await response.json();
            if (response.ok) {
                updateMainDeckGrid(deckId);
                updateExtraDeckGrid(deckId);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error adding card:', error);
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

    // Extra deck cards hover effect
    if (target.matches('.extra-card-slot img')) {
        const cardImgSrc = target.src;
        document.querySelector('.card-view').src = cardImgSrc;

        const cardDescription = target.closest('.extra-card-slot').dataset.cardDescription;
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




// Pagination
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('card-search-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        await fetchCards(0);
    });

    document.getElementById('nextPageBtn').addEventListener('click', async (event) => {
        event.preventDefault();
        await paginate(30);
    });

    document.getElementById('prevPageBtn').addEventListener('click', async (event) => {
        event.preventDefault();
        await paginate(-30);
    });
});

async function fetchCards(offsetChange) {
    const form = document.getElementById('card-search-form');
    const formData = new FormData(form);
    const currentOffset = parseInt(formData.get('offset')) || 0;
    const newOffset = currentOffset + offsetChange;

    formData.set('offset', newOffset);

    try {
        const response = await fetch('/api/cards/search', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();

        if (result.error) {
            console.error(result.error);
            alert('Error searching cards. Please try again later.');
            return;
        }

        // Update the search results container with the new search results
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

        // Update the offset input value
        document.querySelector('input[name="offset"]').value = newOffset;

        // Enable or disable pagination buttons
        document.getElementById('prevPageBtn').disabled = newOffset <= 0;
        document.getElementById('nextPageBtn').disabled = result.pages_remaining === 0;

    } catch (error) {
        console.error('Error searching cards:', error);
        alert('Error searching cards. Please try again later.');
    }
}

async function paginate(offsetChange) {
    const form = document.getElementById('card-search-form');
    const formData = new FormData(form);
    const currentOffset = parseInt(formData.get('offset')) || 0;
    const newOffset = currentOffset + offsetChange;

    formData.set('offset', newOffset);

    await fetchCards(offsetChange);
}

// Reset the offset to 0 when a new search is submitted
document.getElementById('card-search-form').addEventListener('submit', () => {
    const form = event.target;
    form.querySelector('input[name="offset"]').value = 0;
});

// Add event listener to clear filter button
document.getElementById('clear-filters-btn').addEventListener('click', async (event) => {
    const form = document.getElementById('card-search-form');
    form.reset();
    form.querySelector('input[name="offset"]').value = 0;
});

// Submit rename deck form
document.getElementById('submit-rename-form').addEventListener('click', function () {
    document.getElementById('rename-deck-form').submit();
});


// Initial update when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const deckId = getDeckIdFromUrl();
    updateMainDeckGrid(deckId);
    updateExtraDeckGrid(deckId);
});

