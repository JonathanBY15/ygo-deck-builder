<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/JonathanBY15/ygo-deck-builder">
    <img src="static\images\logo-bg-wide.png" alt="Logo" width="480" height="100">
  </a>

  <p align="center">
    A web app for building Yu-Gi-Oh! decks.
    <br />
    <a href="https://github.com/JonathanBY15/ygo-deck-builder">View Demo</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The Yu-Gi-Oh! Deck Builder provides a user-friendly platform for Yu-Gi-Oh! players to build, manage, and analyze their decks. Users can access the entire Yu-Gi-Oh! card database and build their own decks using search, filter, and sort functionalities.

### Features:

* **Deck Building:**
    * Create, edit, save, view, and delete multiple decks.
    * Add and remove cards within a deck.
* **Card Database:**
    * Search and browse the Yu-Gi-Oh! card database.
    * Filters and sorting options.
    * Detailed view of individual cards with stats and descriptions.
* **User Accounts:**
    * Registration and login.
    * Profile management.





### Built With
<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="40" alt="flask logo"  />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" height="40" alt="postgresql logo"  />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="40" alt="javascript logo"  />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="40" alt="html5 logo"  />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="40" alt="css3 logo"  />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" height="40" alt="bootstrap logo"  />
</div>



<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up and run the Yu-Gi-Oh! Deck Builder on your local machine.

### Prerequisites

* <a href="https://www.python.org/downloads/">Python</a>
* <a href="https://www.postgresql.org/download/">PostgreSQL</a>

### Installation

1. Set up the PostgreSQL database.
    ```sh
    psql -U <your_PostgreSQL_username>
   createdb yugioh_deck_builder
   ```
2. Clone the repository.
   ```sh
   git clone https://github.com/JonathanBY15/ygo-deck-builder.git
   ```
3. Create virtual environment.
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Download requirements.
   ```sh
   pip install -r requirements.txt
   ```
5. Run database migrations.
    ```sh
   flask db upgrade
   ```
6. Start the Flask server.
    ```sh
   flask run
   ```

### Access The Application
Once the PostgreSQL database and the Flask server is created, open your web browser and go to:
```arduino
http://localhost:3000
```
You should now see the Yu-Gi-Oh! Deck Builder application running.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The user can add, view, edit, and delete their own decks. They can use filter functionalities to search the YGO card database to build their decks.


<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTACT -->
## Contact
Email: jonathanyaprak@gmail.com
<br />
LinkedIn: [LinkedIn](https://www.linkedin.com/in/jonathan-yaprak/)
<br />
Project Link: [https://github.com/JonathanBY15/ygo-deck-builder](https://github.com/JonathanBY15/ygo-deck-builder)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Yu-Gi-Oh! API by YGOPRODeck](https://ygoprodeck.com/api-guide/)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
