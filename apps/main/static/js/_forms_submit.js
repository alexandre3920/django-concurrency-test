document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll('form').forEach((form) => {
    const submit_button = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', (e) => {
      // Stop the submit request if the form has the is-submitting class
      if (form.classList.contains('is-submitting')) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      } else {
        // Otherwise add the is-submitting class to the form
        form.classList.add('is-submitting');
        // Then disable the submit button
        submit_button.disabled = true;
        // add the disabled class
        submit_button.classList.add('disabled');
      }
    });
  });
});
