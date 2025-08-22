if (!window.parkingSpotHandlersAttached) {
    window.parkingSpotHandlersAttached = true;

    document.addEventListener('DOMContentLoaded', () => {

        const spots = document.querySelectorAll('[data-spot-id]');
        const selectedInput = document.getElementById('selected_spot_id');
        const bookBtn = document.getElementById('bookBtn');

        spots.forEach(spot => {
            spot.addEventListener('click', () => {
                const status = spot.dataset.spotStatus;
                const spotId = spot.dataset.spotId;

                if (status === 'O') return;

                if (selectedInput.value === spotId) {
                    spot.classList.remove('selected');
                    selectedInput.value = null;
                    bookBtn.disabled = true;
                    return;
                }

                spots.forEach(s => s.classList.remove('selected'));
                spot.classList.add('selected');
                selectedInput.value = spotId;
                bookBtn.disabled = false;
            });
        });
    });
};