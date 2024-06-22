# Yu-Gi-Oh! Deck Builder

The goal of the Yu-Gi-Oh! Deck Builder is to provide a user-friendly platform for Yu-Gi-Oh! players to build, manage, and analyze their decks. Users will have access to the entire Yu-Gi-Oh! card database and be able to build multiple decks using search, filter, and sort functionalities.

The app will utilize the [Yu-Gi-Oh! API](https://ygoprodeck.com/api-guide/) to access the card database, providing comprehensive details for every card in the Yu-Gi-Oh! TCG, including ATK, DEF, card descriptions, card images, and more.

## Functionality of the App

- **User Accounts**:
  - Registration and login.
  - Profile management.
  - Password recovery.
- **Deck Building**:
  - Create, edit, save, view, and delete multiple decks.
  - Add and remove cards within a deck.
- **Card Database**:
  - Search and browse the Yu-Gi-Oh! card database.
  - Filters and sorting options.
  - Detailed view of individual cards with stats and descriptions.


## Database Schema

![Database Schema](/capstone1-ss/db_schema.png)

## User Flow

**Homepage**:
   - Options to register, log in, or read about the app.

**Registration/Login**:
   - Sign-up and login forms.

**Decks**:
   - List of user's decks.
   - View, edit, and delete saved decks.
   - Quick links to create a new deck or access existing ones.

**Deck Builder**:
   - Visual representation of the deck.
   - Interface for adding cards to the deck.
   - Search bar with filters and sort options.
   - Detailed card views.

## Potential Issues with the API

- **Multiple Versions of a Card**: Some cards in the API have multiple versions with different images. This should be handled by either displaying only one version of the card or letting the user select which version of the card they would like.

- **Limitation:** The API has a rate limit of 20 requests per second. Exceeding this limit will result in being blocked from accessing the API for 1 hour. This shouldn't be a problem considering the anticipated user base of the project.

## Sensitive Information to Secure

- **User Data**:
  - Personal information such as passwords must be hashed and stored using encryption methods.
- **Session Data**:
  - Manage authentication tokens securely to prevent unauthorized access to a users decks.