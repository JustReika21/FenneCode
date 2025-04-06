(function () {
  if (document.getElementById('globalCustomAlert')) return;

  const wrapper = document.createElement('div');
  wrapper.id = 'globalCustomAlert';
  wrapper.className = 'custom-alert hidden';
  wrapper.innerHTML = `
    <div class="custom-alert-box">
      <p id="customAlertMessage">Alert</p>
      <button id="customAlertOkBtn" class="custom-alert-button">OK</button>
    </div>
  `;
  document.body.appendChild(wrapper);

  window.alert = function (message) {
    return new Promise((resolve) => {
      document.getElementById('customAlertMessage').textContent = message;
      wrapper.classList.remove('hidden');

      const okBtn = document.getElementById('customAlertOkBtn');

      const close = () => {
        wrapper.classList.add('hidden');
        okBtn.removeEventListener('click', close);
        resolve();
      };

      okBtn.addEventListener('click', close);
    });
  };

  window.showToast = function (message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'custom-toast';
    toast.innerHTML = `
      <div class="toast-message">${message}</div>
      <div class="toast-timer" style="animation-duration: ${duration}ms;"></div>
    `;

    const containerId = 'toast-container';
    let container = document.getElementById(containerId);

    if (!container) {
      container = document.createElement('div');
      container.id = containerId;
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('hide');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  };
})();