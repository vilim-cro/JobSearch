let counter = 1;
const quantity = 10;

document.addEventListener('DomContentLoaded', load());

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
}

function load() {
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;
    console.log(counter);

    fetch(`/load?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.jobs.forEach(add_jobs);
    });
}

function add_jobs(job) {
    console.log(job);
}