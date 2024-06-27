// Scripts will be written here


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
