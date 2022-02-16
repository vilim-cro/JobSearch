let counter = 1;
const quantity = 10;

document.addEventListener('DomContentLoaded', load());

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight && counter <= 20) {
        load();
    }
}

function load() {
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    pars = {};
    window.location.search.substr(1).split('&').forEach(data => {
      lista = data.split('=');
      pars[lista[0]] = lista[1];
    })

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

  const card_button = document.createElement('button');
  card_button.className = "btn btn-primary";
  card_button.innerHTML = "View more";
  card_button.onclick = load_page;
  card_body.append(card_button);

  card.append(card_body);

  document.querySelector('.cards').append(card);
}

function load_page() {
  //fetch(`{this.id}`)
}