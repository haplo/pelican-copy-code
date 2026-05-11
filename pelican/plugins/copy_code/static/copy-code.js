function initCopyButtons() {
  var settingsElement = document.getElementById('copy-code-settings');
  var buttonText = 'Copied!';
  if (settingsElement) {
    buttonText = settingsElement.dataset.buttonText || buttonText;
  }

  document.querySelectorAll('.code-block-wrapper .copy-button').forEach(function (button) {
    button.addEventListener('click', function () {
      var wrapper = button.parentNode;
      var pre = wrapper.querySelector('pre');
      if (!pre) return;

      navigator.clipboard.writeText(pre.textContent).then(function () {
        var originalText = button.textContent;
        button.textContent = ' ' + buttonText;
        button.classList.add('copied');

        setTimeout(function () {
          button.classList.remove('copied');
          button.textContent = originalText;
        }, 2000);
      });
    });
  });
}

document.addEventListener('DOMContentLoaded', initCopyButtons);
