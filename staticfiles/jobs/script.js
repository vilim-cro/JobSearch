// Calculates how many job posts will be rendered
let counter = 1;
const quantity = 10;
let loaded = false;

document.addEventListener('DomContentLoaded', load());

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight && counter <= 20) {
        load();
    }
}

// Renders job posts
function load() {
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    pars = {};
    window.location.search.substr(1).split('&').forEach(data => {
      let lista = data.split('=');
      pars[lista[0]] = lista[1];    // Stores j and l search parameters
    })

    let list = window.location.href.split('/');
    if (list[list.length - 1] == "myposts") {     // Checks if the page is 'myposts'
      if (!loaded) {
        loaded = true;
        fetch(`/users/myjobs`)              // Only renders job posts of authenticated user
        .then(response => response.json())
        .then(data => {
          if (data.length == 0) {
            let h3 = document.createElement('h3');
            h3.innerHTML = "You have no job posts yet."
            document.querySelector('.message').append(h3);
          }
          data.forEach(add_jobs);
      });
      }
    }

    // Renders searched job posts on find page, infinite scroll
    else {
      if (pars['j'] != undefined) {
        fetch(`/jobs/load?start=${start}&end=${end}&j=${pars['j']}&l=${pars['l']}`)
        .then(response => response.json())
        .then(data => {
          data.forEach(add_jobs);
      });
      }
      else {
        fetch(`/jobs/load?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
          data.forEach(add_jobs);
      });
    }
  }
}

// Takes the job as JSON and creates div job card
function add_jobs(job) {
  const card = document.createElement('div');
  card.className = 'card';

  const card_body = document.createElement('div');
  card_body.className = 'card-body';

  const card_title = document.createElement('h5');
  card_title.className = 'card-title';
  card_title.innerHTML = job.fields.jobtitle;
  card_body.append(card_title);

  const card_text = document.createElement('p');
  card_text.className = 'card-text';
  card_text.innerHTML = job.fields.location;
  card_body.append(card_text);

  const card_span = document.createElement('span');
  card_span.style.display = "flex";
  card_span.style.justifyContent = "space-between";

  const card_button = document.createElement('button');
  card_button.className = "btn btn-primary";
  card_button.innerHTML = "View more";
  card_button.dataset.toggle = "modal";
  card_button.dataset.target = "#exampleModal";

  card_button.onclick = function() {    // Js for modal from bootstrap

    let modalTitle = document.querySelector('.modal-title');
    modalTitle.innerHTML = job.fields.jobtitle + " - " + job.fields.location;
    let des = document.querySelector('#des');
    des.innerHTML = job.fields.description;
    let about = document.querySelector('#about');
    about.innerHTML = job.fields.about;
  }
  
  card_span.append(card_button);
  

  let list = window.location.href.split('/');     // If the page is 'myposts', adds delete button and new modal
  if (list[list.length - 1] == "myposts") {
    const card_button_danger = document.createElement('button');
    card_button_danger.className = "btn btn-danger";
    card_button_danger.innerHTML = "Delete";
    card_button_danger.dataset.toggle = "modal";
    card_button_danger.dataset.target = "#exampleModalCenter";
    card_button_danger.onclick = () => {
      document.querySelector('#delete-modal').innerHTML = `Are you sure you want to delete "${job.fields.jobtitle}" job post?`;
      document.querySelector('#delete-button').href = `/users/${job.pk}`;
    }
  
    card_span.append(card_button_danger);
  }

  card_body.append(card_span);
  card.append(card_body);

  document.querySelector('.cards').append(card);
}

