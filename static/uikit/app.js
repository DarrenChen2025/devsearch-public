// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();

  
// });

let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

//auto close the flash message after 5 seconds
if (alertWrapper) {
  setTimeout(function() {
    alertWrapper.style.display = "none";
  }, 5000); // 5000 milliseconds = 5 seconds
}

function closeButton() {
  alertWrapper.style.display = "none"
}

document.addEventListener('DOMContentLoaded', function() {
  let alertCloses = document.querySelectorAll('.alert__close');
  alertCloses.forEach(alertClose => {
      alertClose.addEventListener('click', closeButton);
  });
});
