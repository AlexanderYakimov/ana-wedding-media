// Array to hold all photos, current index, offset, and loading flag
let photos = [];
let currentIndex = 0;
let offset = 0;
let limit = 12;
let totalPhotos = 0;
let isLoading = false;

/**
 * Function to calculate the limit of photos to load based on the current window size.
 * @returns {number} The limit of photos to load.
 */
function calculateLimit() {
    const screenHeight = document.documentElement.clientHeight || window.innerHeight;
    const cardHeight = 250; // Height of a card
    const cardsPerRow = Math.floor($('#gallery').width() / 250); // Number of cards in a row
    const rowsPerScreen = Math.ceil(screenHeight / cardHeight); // Number of rows visible
    return Math.max(cardsPerRow * rowsPerScreen * 3, 12); // At least 12 images
}

/**
 * Function to load photos from the server.
 */
function loadPhotos(callback) {
    if (isLoading) return;

    isLoading = true;
    $('#loading').show();

    $.getJSON('/api/photos', { limit: limit, offset: offset }, function (response) {
        const newPhotos = response.files;
        if (newPhotos.length === 0) {
            $('#loading').text('Больше фотографий нет').fadeOut(2000);
            $('#loadMoreButton').hide();
            return;
        }

        totalPhotos = response.total;
        let gallery = $('#gallery');
        newPhotos.forEach(photo => {
            if (!photos.includes(photo)) {
                photos.push(photo);
                const card = `
                    <div class="col">
                        <div class="card">
                            <img src="/download/${photo}" alt="${photo}" data-bs-toggle="modal" 
                                 data-bs-target="#photoModal" data-index="${photos.length - 1}">
                        </div>
                    </div>`;
                gallery.append(card);
            }
        });

        offset += limit;
        isLoading = false;
        $('#loading').hide();
        if (callback) callback();
    }).fail(function () {
        $('#loading').text('Ошибка загрузки. Попробуйте ещё раз.').fadeOut(2000);
        isLoading = false;
    });
}

/**
 * Function to update the modal with the current photo and its counter.
 */
function updateModal() {
    if (currentIndex < 0 || currentIndex >= photos.length) {
        console.error("Invalid photo index");
        return;
    }
    const photo = photos[currentIndex];
    const src = `/download/${photo}`;
    $('#modalImage').attr('src', src);
    $('#photoCounter').text(`${currentIndex + 1} из ${totalPhotos}`);
}

$(document).ready(function () {
    limit = calculateLimit();
    loadPhotos();

    // Photo click event to show modal
    $('#gallery').on('click', 'img', function () {
        const index = $(this).data('index');
        if (index === undefined) {
            console.error("index not found for the clicked image");
            return;
        }
        currentIndex = index;
        updateModal();
        $('#photoModal').modal('show');
    });

    // Previous photo button
    $('#prevPhoto').click(function () {
        if (currentIndex > 0) {
            currentIndex--;
            updateModal();
        }
    });

    // Next photo button
    $('#nextPhoto').click(function () {
        if (currentIndex < photos.length - 1) {
            currentIndex++;
            updateModal();
        } else if (!isLoading) {
            loadPhotos(() => {
                if (currentIndex < photos.length - 1) {
                    currentIndex++;
                    updateModal();
                }
            });
        }
    });

    // Download button
    $('#downloadPhoto').click(function () {
        const photo = photos[currentIndex];
        const link = document.createElement('a');
        link.href = `/download/${photo}`;
        link.download = photo;
        link.click();
    });

    // "Load More" button click event
    $('#loadMoreButton').click(function () {
        loadPhotos();
    });
});
