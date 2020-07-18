const new_post = document.getElementById('new_post');
const add_tag_form = document.getElementById('add_tag_form');
const add_tag_input = document.getElementById('add_tag');
const tag_fields = document.getElementById('tag_fields');
const post_form = document.getElementById('post_form');
const next = document.getElementById('next');
const title = document.getElementById('title');
const slug = document.getElementById('slug');
const summary = document.getElementById('summary');
const body = document.getElementById('body');

const deleteTag = (event) => {
  event.originalTarget.parentElement.remove();
};

const addTag = (tagName) => {
  const field = document.createElement('div');
  field.className = 'control';
  tag_fields.appendChild(field);
  const tags_addons = document.createElement('div');
  tags_addons.className = 'tags has-addons';
  field.appendChild(tags_addons);
  const tag = document.createElement('p');
  tag.innerText = tagName;
  tag.className = 'tag is-link';
  const tag_delete = document.createElement('a');
  tag_delete.className = 'tag is-delete';
  tag_delete.addEventListener('click', deleteTag, false);
  tags_addons.appendChild(tag);
  tags_addons.appendChild(tag_delete);
  add_tag_input.value = '';
};

add_tag_input.addEventListener('keyup', function(e) {
  if (e.keyCode == 13) {
    addTag(add_tag_input.value);
  }
});

title.addEventListener('keyup', function() {
  document.getElementById('slug').value = title.value.replace(/\s+/g, '-').toLowerCase();
});

let valid = true;


next.addEventListener('click', (e) => {
  // Get all elements with the input type of text
  const inputs = document.querySelectorAll('input[type="text"], textarea');
  inputs.forEach(input => {
    if (input.nextElementSibling != null) {
      input.nextElementSibling.remove();
      input.classList.remove('is-danger');
    }
    if (input.value.length == 0) {
      input.classList.add('is-danger');
      const message = document.createElement('p');
      message.innerHTML = 'This field is required.';
      message.className = 'help is-danger';
      input.parentElement.appendChild(message);
      valid = false;
    } else {
      valid = true;
    }
  });

  if (valid) {
    next.classList.add('is-loading');
    async function postData(url = '', data = {}) {
      // Default options are marked with *
      const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
      return response.json(); // parses JSON response into native JavaScript objects
    }

    let tags = [];
    document.querySelectorAll('.tag.is-link').forEach(tag => {
      tags.push(tag.innerText);
    })
    const post = {
      "title": title.value,
      "body": body.value,
      "slug": slug.value,
      "summary": summary.value,
      "tags": tags
    };

    postData('http://localhost:5000/new_post/', post)
      .then(data => {
          next.classList.remove('is-loading');
          document.getElementById('step-two').classList.add('is-active');
          console.log(data); // JSON data parsed by `data.json()` call
      }).catch(error => {
          next.classList.remove('is-loading');
          console.log(error);
          alert('error!');
      });
  }
});

