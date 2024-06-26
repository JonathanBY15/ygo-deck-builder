// function addToDeck(deckId, cardId) {
//     // Fetch API endpoint to add card to deck
//     fetch(`/decks/${deckId}/cards/add/${cardId}`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             deckId: deckId,
//             cardId: cardId
//         })
//     })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Handle success message or redirection as needed
//             console.log(data.message); // Display success message
//             window.location.href = `/decks/${deckId}`; // Redirect to deck page
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             // Handle error or display error message to user
//         });
// }
