document.addEventListener('DOMContentLoaded', function () {
    const calendarContainer = document.getElementById('calendar');
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Create day containers
    days.forEach(day => {
        const dayContainer = document.createElement('div');
        dayContainer.classList.add('col-md-4', 'mb-4'); // Adjust column size as needed
        dayContainer.innerHTML = `<h4>${day}</h4><div class="events-container" style="max-height: 200px; overflow-y: auto;"></div>`;
        calendarContainer.appendChild(dayContainer);
    });

    // Fetch events from the server
    fetch('/events')
        .then(response => response.json())
        .then(events => {
            // Populate events into day containers
            events.forEach(event => {
                const startDateTime = new Date(event.start);
                const dayIndex = startDateTime.getDay();
                const dayContainer = calendarContainer.children[dayIndex];
                const eventsContainer = dayContainer.querySelector('.events-container');

                const eventElement = document.createElement('div');
                eventElement.classList.add('card', 'mb-3');
                eventElement.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${event.summary}</h5>
                        <p class="card-text">Start: ${formatDateTime(startDateTime)}</p>
                        <p class="card-text">End: ${formatDateTime(new Date(event.end))}</p>
                    </div>
                `;
                eventsContainer.appendChild(eventElement);
            });
        })
        .catch(error => console.error('Error fetching events:', error));

    // Function to format date and time
    function formatDateTime(dateTime) {
        return dateTime.toLocaleString('en-US', {
            month: 'long',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    }
});
