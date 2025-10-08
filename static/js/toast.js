toast.js
function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toastComponent) return;

    // reset
    toastComponent.classList.remove(
        'bg-red-50','border-red-500','text-red-600',
        'bg-green-50','border-green-500','text-green-600',
        'bg-yellow-50','border-yellow-500','text-yellow-600',
        'bg-cyan-50','border-cyan-500','text-cyan-600',
        'bg-white','border-gray-300','text-gray-800'
    );

    // styles
    if (type === 'success') {
        toastComponent.classList.add('bg-green-50','border-green-500','text-green-600');
        toastComponent.style.border = '1px solid #22c55e';
        if (toastIcon) toastIcon.textContent = '✅';
    } else if (type === 'error') {
        toastComponent.classList.add('bg-red-50','border-red-500','text-red-600');
        toastComponent.style.border = '1px solid #ef4444';
        if (toastIcon) toastIcon.textContent = '⛔';
    } else if (type === 'warning') {
        toastComponent.classList.add('bg-yellow-50','border-yellow-500','text-yellow-600');
        toastComponent.style.border = '1px solid #eab308';
        if (toastIcon) toastIcon.textContent = '⚠';
    } else if (type === 'info') {
        toastComponent.classList.add('bg-cyan-50','border-cyan-500','text-cyan-600');
        toastComponent.style.border = '1px solid #06b6d4';
        if (toastIcon) toastIcon.textContent = 'ℹ';
    } else {
        toastComponent.classList.add('bg-white','border-gray-300','text-gray-800');
        toastComponent.style.border = '1px solid #d1d5db';
        if (toastIcon) toastIcon.textContent = '💬';
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    toastComponent.classList.remove('opacity-0','translate-y-64');
    toastComponent.classList.add('opacity-100','translate-y-0');

    setTimeout(() => {
        toastComponent.classList.remove('opacity-100','translate-y-0');
        toastComponent.classList.add('opacity-0','translate-y-64');
    }, duration);
}